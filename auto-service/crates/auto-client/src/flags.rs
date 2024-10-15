pub const IP: &str = "127.0.0.1";
pub const PORT: u16 = 10086;

#[derive(clap::Parser)]
#[command(name = "AutoServer")]
#[command(about = "AutoServer is my own server", long_about = None)]
pub struct Flags {
    /// server listening ip addr
    #[arg(long, help = "server listening ip addr", default_value = IP)]
    pub ip: String,

    /// server listening ip port
    #[arg(short, long, default_value_t = PORT, help = "server listening ip port")]
    port: u16,

    /// 子命令
    #[command(subcommand)]
    pub command: Option<Commands>,
}

/// 子命令枚举
#[derive(clap::Subcommand)]
pub enum Commands {
    #[command(name = "ip_service", about = "ip service")]
    IpService {
        #[command(subcommand)]
        command: Option<IpServiceCommand>,
    },
}

#[derive(clap::Subcommand)]
pub enum IpServiceCommand {
    #[command(
        name = "add_remote",
        about = "add_remote request add client ip to server"
    )]
    AddRemote {},
    #[command(name = "list", about = "list client ip request to server")]
    List {},
    #[command(
        name = "monitor_ip",
        about = "monitor the client ip addr, if changed, tell the new ip to the server"
    )]
    MonitorIp {},
}
