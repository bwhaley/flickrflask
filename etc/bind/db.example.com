$TTL     300
@     IN     SOA     example.com. admin.example.com. (
                     4          ; Serial
                604800          ; Refresh
                 86400          ; Retry
               2419200          ; Expire
                 86400 )     ; Negative Cache TTL
                        NS      dns1.example.com.
                        A       10.0.1.25
$ORIGIN example.com.
bastion     IN     A      10.0.0.82
web1     IN     A     10.0.1.65
web2     IN     A     10.0.1.115
db1     IN     A     10.0.1.32
db2     IN     A     10.0.1.66
lb1     IN     A     10.0.0.101
dns1     IN     A     10.0.1.25
monitoring     IN     A     10.0.1.106

