use service_protos::proto_ip_service::NetDevice;

#[cfg(target_os = "linux")]
pub async fn get_net_info() -> Vec<NetDevice> {
    let devices = get_net_devices().await;
    let mut args = vec!["addr".to_string(), "show".to_string()];
    let mut net_devices: Vec<NetDevice> = Vec::new();
    for device in devices {
        args.push(device.clone());
        let (stdout, _stderr) = common::command::Command::run("ip".to_string(), args.clone()).await;
        let ips = parse_ip_addr(stdout.as_str());
        let mac = parse_mac_addr(stdout.as_str());
        net_devices.push(NetDevice { device, mac, ips });
        args.pop();
    }
    net_devices
}

#[cfg(target_os = "linux")]
async fn get_net_devices() -> Vec<String> {
    let (stdout, _stderr) = common::command::Command::run(
        "ip".to_string(),
        vec!["link".to_string(), "show".to_string()],
    )
    .await;
    let devices = parse_net_devices(stdout.as_str());
    devices
}

#[cfg(target_os = "linux")]
fn parse_net_devices(ip_link_show: &str) -> Vec<String> {
    let net_devices = ip_link_show
        .split('\n')
        .filter_map(|line| {
            let line = line.trim_start();
            match line.strip_prefix("link") {
                Some(_) => None,
                None => {
                    let mut iter = line.split(": ");
                    iter.next();
                    iter.next().map(|dev| dev.to_string())
                }
            }
        })
        .collect::<Vec<String>>();
    net_devices
}

#[cfg(target_os = "linux")]
fn parse_ipv4_addr(ip_addr_show: &str) -> Vec<String> {
    ip_addr_show
        .split('\n')
        .filter_map(|line| {
            line.trim_start()
                .strip_prefix("inet ")
                .and_then(|s| s.split_whitespace().next())
                .map(|addr| addr.to_string()) // 将 &str 转换为 String
        })
        .collect::<Vec<String>>()
}

#[cfg(target_os = "linux")]
fn parse_ipv6_addr(ip_addr_show: &str) -> Vec<String> {
    ip_addr_show
        .split('\n')
        .filter_map(|line| {
            line.trim_start()
                .strip_prefix("inet6 ")
                .and_then(|s| s.split_whitespace().next())
                .map(|addr| addr.to_string()) // 将 &str 转换为 String
        })
        .collect::<Vec<String>>()
}

#[cfg(target_os = "linux")]
fn parse_ip_addr(ip_addr_show: &str) -> Vec<String> {
    let mut ipv4 = parse_ipv4_addr(ip_addr_show);
    let mut ipv6 = parse_ipv6_addr(ip_addr_show);
    let mut ip: Vec<String> = Vec::new();
    ip.append(&mut ipv4);
    ip.append(&mut ipv6);
    ip
}

#[cfg(target_os = "linux")]
fn parse_mac_addr(ip_addr_show: &str) -> String {
    ip_addr_show
        .split('\n')
        .filter_map(|line| {
            line.trim_start().strip_prefix("link/").and_then(|mac| {
                let mut s = mac.split_whitespace();
                s.next();
                s.next()
            })
        })
        .collect::<String>()
}

#[cfg(target_os = "windows")]
pub async fn get_net_info() {
    todo!();
}
