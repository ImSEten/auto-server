use service_protos::proto_ip_service::ip_server::Ip;

#[derive(Default)]
pub struct IpServer {}

#[tonic::async_trait]
impl Ip for IpServer {}
