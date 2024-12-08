from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import  dict_factory

class ScyllaClient():
    
    def __init__(self, config):
        self.cluster = self._get_cluster(config)
        self.session = self.cluster.connect(config.KEYSPACE)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown()
        
    def shutdown(self):
        self.cluster.shutdown()

    def _get_cluster(self, config):
        profile = ExecutionProfile(
            load_balancing_policy=TokenAwarePolicy(
                    DCAwareRoundRobinPolicy(local_dc=config.DATACENTER)
                ),
                row_factory=dict_factory
            )
        return Cluster(
            execution_profiles={EXEC_PROFILE_DEFAULT: profile},
            contact_points=[config.HOST],
            auth_provider = PlainTextAuthProvider(username=config.USER,
                                                  password=config.PASSWORD))
    
    def print_metadata(self):
        for host in self.cluster.metadata.all_hosts():
            print(f"Datacenter: {host.datacenter}; Host: {host.address}; Rack: {host.rack}")
    
    def get_session(self):
        return self.session
