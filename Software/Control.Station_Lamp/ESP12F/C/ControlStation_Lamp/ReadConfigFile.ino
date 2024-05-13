

#define CONTROL_FILE_NAME "/control_config.json"
#define BUFF_SIZE 1024

// --- Config file ---
//String essid;
//String password;
//String webserver_ip;
//String webserver_path_info_timestamp;
//String webserver_path_lamp_register;
//String webserver_path_info_is_alive;
//
//String lamp_id;
//int lamp_gpio;
//int led_status_gpio;
//int led_status_inverse;
//int register_interval_sec;
//int regular_reset_seconds;
// -------------------

bool loadConfig(){
  File configFile = SPIFFS.open(CONTROL_FILE_NAME, "r");
  if( !configFile){
    Serial.println("Failed to open config file for reading");
    return false;
  }

  size_t size = configFile.size();
  if(size > BUFF_SIZE){
    configFile.close();
    Serial.println("config file size is too large");
    return false;
  }

  Serial.print("File size: ");
  Serial.println(size);

  std::unique_ptr<char[]> buf(new char[size]);
  configFile.readBytes(buf.get(), size);  
  Serial.println(buf.get());

  StaticJsonDocument<1024> doc;
  DeserializationError error = deserializeJson(doc, buf.get());

  if(error){
    Serial.print("Failed to parse config file: ");
    Serial.println(error.c_str());
    return false;
  }

  configFile.close();

  essid = String(doc["central-ap"]["essid"]);
  password = String(doc["central-ap"]["password"]);
  webserver_ip = String(doc["central-ap"]["webserver-ip"]);
  webserver_path_info_timestamp = String(doc["central-ap"]["webserver-path-info-timestamp"]);
  webserver_path_lamp_register = String(doc["central-ap"]["webserver-path-lamp-register"]);
  webserver_path_info_is_alive = String(doc["central-ap"]["webserver-path-info-is-alive"]);
  
  lamp_id = String(doc["control-sta"]["lamp-id"]);
  lamp_gpio = doc["control-sta"]["lamp-gpio"];
  led_status_gpio = doc["control-sta"]["led-status-gpio"];
  led_status_inverse = doc["control-sta"]["led-status-inverse"];
  register_interval_sec = doc["control-sta"]["register-interval-sec"];
  regular_reset_seconds = doc["control-sta"]["regular-reset-seconds"];

  // ---

  Serial.print("central-ap.essid = ");
  Serial.println(essid);

  Serial.print("central-ap.password = ");
  Serial.println(password);

  Serial.print("central-ap.webserver-ip = ");
  Serial.println(webserver_ip);
  
  Serial.print("central-ap.webserver-path-info-timestamp = ");
  Serial.println(webserver_path_info_timestamp);
  
  Serial.print("central-ap.webserver-path-lamp-register = ");
  Serial.println(webserver_path_lamp_register);
  
  Serial.print("central-ap.webserver-path-info-is-alive = ");
  Serial.println(webserver_path_info_is_alive);

  Serial.print("control-sta.lamp-id = ");
  Serial.println(lamp_id);

  Serial.print("control-sta.lamp-gpio = ");
  Serial.println(lamp_gpio);

  Serial.print("control-sta.led-status-gpio = ");
  Serial.println(led_status_gpio);
  
  Serial.print("control-sta.led-status-inverse = ");
  Serial.println(led_status_inverse);
  
  Serial.print("control-sta.register-interval-sec = ");
  Serial.println(register_interval_sec);

  Serial.print("control-sta.regular-reset-seconds = ");
  Serial.println(regular_reset_seconds);

  return true;
}
