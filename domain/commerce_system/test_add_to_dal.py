from data_access_layer.subscribed_repository import save_subscribed
from domain.commerce_system.user import Subscribed
import data_access_layer.init_tables

sub = Subscribed("Ttt")
save_subscribed(sub, Subscribed)