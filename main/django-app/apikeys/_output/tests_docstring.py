class TestCase(TransactionTestCase):
    """
    Similar to TransactionTestCase, but use `transaction.atomic()` to achieve
    test isolation.

    In most situations, TestCase should be preferred to TransactionTestCase as
    it allows faster execution. However, there are some situations where using
    TransactionTestCase might be necessary (e.g. testing some transactional
    behavior).

    On database backends with no transaction support, TestCase behaves as
    TransactionTestCase.
    """

    @classmethod
    def _enter_atomics(cls):
        """Open atomic blocks for multiple databases."""
        atomics = {}
        for db_name in cls._databases_names():
            atomic = transaction.atomic(using=db_name)
            atomic._from_testcase = True
            atomic.__enter__()
            atomics[db_name] = atomic
        return atomics

    @classmethod
    def _rollback_atomics(cls, atomics):
        """Rollback atomic blocks opened by the previous method."""
        for db_name in reversed(cls._databases_names()):
            transaction.set_rollback(True, using=db_name)
            atomics[db_name].__exit__(None, None, None)

    @classmethod
    def _databases_support_transactions(cls):
        return connections_support_transactions(cls.databases)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls._databases_support_transactions():
            return
        cls.cls_atomics = cls._enter_atomics()

        if cls.fixtures:
            for db_name in cls._databases_names(include_mirrors=False):
                try:
                    call_command(
                        "loaddata",
                        *cls.fixtures,
                        **{"verbosity": 0, "database": db_name},
                    )
                except Exception:
                    cls._rollback_atomics(cls.cls_atomics)
                    raise
        pre_attrs = cls.__dict__.copy()
        try:
            cls.setUpTestData()
        except Exception:
            cls._rollback_atomics(cls.cls_atomics)
            raise
        for name, value in cls.__dict__.items():
            if value is not pre_attrs.get(name):
                setattr(cls, name, TestData(name, value))

    @classmethod
    def tearDownClass(cls):
        if cls._databases_support_transactions():
            cls._rollback_atomics(cls.cls_atomics)
            for conn in connections.all(initialized_only=True):
                conn.close()
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        """Load initial data for the TestCase."""
        pass

    def _should_reload_connections(self):
        if self._databases_support_transactions():
            return False
        return super()._should_reload_connections()

    def _fixture_setup(self):
        if not self._databases_support_transactions():
            # If the backend does not support transactions, we should reload
            # class data before each test
            self.setUpTestData()
            return super()._fixture_setup()

        if self.reset_sequences:
            raise TypeError("reset_sequences cannot be used on TestCase instances")
        self.atomics = self._enter_atomics()

    def _fixture_teardown(self):
        if not self._databases_support_transactions():
            return super()._fixture_teardown()
        try:
            for db_name in reversed(self._databases_names()):
                if self._should_check_constraints(connections[db_name]):
                    connections[db_name].check_constraints()
        finally:
            self._rollback_atomics(self.atomics)

    def _should_check_constraints(self, connection):
        return (
            connection.features.can_defer_constraint_checks
            and not connection.needs_rollback
            and connection.is_usable()
        )

    @classmethod
    @contextmanager
    def captureOnCommitCallbacks(cls, *, using=DEFAULT_DB_ALIAS, execute=False):
        """Context manager to capture transaction.on_commit() callbacks."""
        callbacks = []
        start_count = len(connections[using].run_on_commit)
        try:
            yield callbacks
        finally:
            while True:
                callback_count = len(connections[using].run_on_commit)
                for _, callback in connections[using].run_on_commit[start_count:]:
                    callbacks.append(callback)
                    if execute:
                        callback()

                if callback_count == len(connections[using].run_on_commit):
                    break
                start_count = callback_count
    """Similar to TransactionTestCase, but use `transaction.atomic()` to achieve
test isolation.

In most situations, TestCase should be preferred to TransactionTestCase as
it allows faster execution. However, there are some situations where using
TransactionTestCase might be necessary (e.g. testing some transactional
behavior).

On database backends with no transaction support, TestCase behaves as
TransactionTestCase."""

