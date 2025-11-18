import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: "http://localhost:8080",    
  realm: "mvl",                 
  clientId: "mvl-spa",        
});

export default keycloak;
