class ConfigFields:
    PAYMENT_SYSTEM_URL = "payment_system_url"
    DELIVERY_SYSTEM_URL = "delivery_system_url"
    # PAYMENT_FACADE = "payment_facade"
    # DELIVERY_FACADE = "delivery_facade"
    # DATABASE_URL = "database_url"
    # DATABASE_CREDENTIALS = "database_credentials"
    # DATABASE_USERNAME = "username"
    # DATABASE_PASSWORD = "password"
    # ADMIN_CREDENTIALS = "admin_credentials"
    # ADMIN_USERNAME = "username"
    # ADMIN_PASSWORD = "password"
    # CERTIFICATE_PATH = "certificate_path"
    # CERTIFICATE = "cert"
    # KEY = "key"
    # SEVER_PORT = "port"
    # NOTIFICATIONS_COMPONENT = "notifications"


config = {
    ConfigFields.PAYMENT_SYSTEM_URL: "http://localhost/",
    ConfigFields.DELIVERY_SYSTEM_URL: "http://localhost/",
}
