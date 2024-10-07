use async_trait::async_trait;
use std::collections::HashMap;

#[async_trait]
pub trait Services {
    async fn set_client_info<T>(&self, request: tonic::Request<T>)
    where
        T: Send;

    async fn get_client_info<T>(&self, request: &tonic::Request<T>) -> (String, String)
    where
        T: Send + std::marker::Sync;
}

#[derive(Default, Debug)]
pub struct CommonClient {
    pub conn_client: HashMap<String, String>,
}

impl CommonClient {
    pub fn set_client(&mut self, ip: String, hostname: String) {
        self.conn_client.insert(ip, hostname);
    }

    pub fn remove_client(&mut self, ip: String) {
        self.conn_client.remove(&ip);
    }
}
