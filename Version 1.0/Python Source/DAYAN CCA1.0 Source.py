import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog , Tk , Label
from netmiko import ConnectHandler
import time
import easygui



class CiscoSwitchManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Cisco Configuration Assistant | DAYAN TEC.")
        self.root.geometry("1366x768")
        self.connection = None
        self.create_main_page()
        root.state("zoomed")


    def create_main_page(self):
        self.clear_frame()
        
        tk.Label(self.root, text="نرم افزار مدیریت سوئیچ های سیسکو", font=("B Titr", 25)).pack(pady=20)

        tk.Label(self.root, text="دستگاه IP آدرس :", font=("Calibri", 14)).pack(pady=5)
        self.switch_ip = tk.Entry(self.root, width=30)
        self.switch_ip.pack(pady=5)

        tk.Label(self.root, text="نام کاربری دستگاه :", font=("Calibri", 14)).pack(pady=5)
        self.username = tk.Entry(self.root, width=30)
        self.username.pack(pady=5)

        tk.Label(self.root, text="Enable Password :", font=("Calibri", 14)).pack(pady=5)
        self.enable_password = tk.Entry(self.root, width=30, show='*')
        self.enable_password.pack(pady=5)

        tk.Label(self.root, text="Secret Password :", font=("Calibri", 14)).pack(pady=5)
        self.secret_password = tk.Entry(self.root, width=30, show='*')
        self.secret_password.pack(pady=5)


        tk.Label(self.root, text="نوع پروتکل اتصال :", font=("Calibri", 14)).pack(pady=5)
        self.protocol = tk.StringVar(value='ssh')
        tk.Radiobutton(self.root, text="SSH   ", variable=self.protocol, value='ssh').pack(pady=0)
        tk.Radiobutton(self.root, text="Telnet", variable=self.protocol, value='telnet').pack(pady=0)

        tk.Button(self.root, text="برقراری ارتباط",font=("Calibri", 14),command=self.connect_to_switch, bg="green", fg="white", width=25, height=1).pack(pady=5)
        tk.Button(self.root, text="خروج ",font=("Calibri", 14),command=self.root.quit, bg="red", fg="white", width=25, height=1).pack(pady=5)
        tk.Button(self.root, text="راهنما",font=("Calibri", 14),command=self.show_help, bg="blue", fg="white", width=25, height=1).pack(pady=5)
        tk.Label(self.root, text="Powered by dayan technology co. | 2024-2025", font=("Calibri", 10)).pack(pady=5)
 




    def connect_to_switch(self):
        ip = self.switch_ip.get()
        username = self.username.get()
        enable_pw = self.enable_password.get()
        secret_pw = self.secret_password.get()
        protocol = self.protocol.get()

        if protocol == "ssh":
            device = {
                'device_type': 'cisco_ios',
                'host': ip,
                'username': username,
                'password': enable_pw,
                'secret': secret_pw,
                'port': 22,
                'timeout': 20,
                "delay_factor_compat": True,
                "fast_cli": False,
            }
            try:
                self.connection = ConnectHandler(**device)
                self.connection.enable()
                self.create_management_page()
            except Exception as e:
                messagebox.showerror("خطا", str(e))
        else:
            device = {
                'device_type': 'cisco_ios_telnet',
                'host': ip,
                'username': username,
                'password': enable_pw,
                'secret': secret_pw,
                'port': 23,
                'timeout': 20,
                "delay_factor_compat": True,
                "fast_cli": False,
            }
            try:
                self.connection = ConnectHandler(**device)
                self.connection.enable()
                self.create_management_page()
            except Exception as e:
                messagebox.showerror("خطا", str(e))



    def create_management_page(self):
        self.clear_frame()
        tk.Label(self.root, text="منو مدیریت سوئیچ", font=("B Titr", 24)).pack(pady=20)

        frame1=tk.Frame(self.root)
        frame1.pack(pady=5)
        tk.Button(frame1, text="Interface خاموش کردن", command=self.shutdown_interface, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame1, text="Interface روشن کردن", command=self.no_shutdown_interface, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame1, text="VLAN به Interface اضافه کردن ", command=self.add_interface_to_vlan, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame1, text="تهیه نسخه پشتیبان", command=self.backup_config, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame1, text="راه اندازی مجدد", command=self.reboot_switch, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)

        frame2=tk.Frame(self.root)
        frame2.pack(pady=5)
        tk.Button(frame2, text="هاInterface وضعیت", command=self.show_interfaces, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT, padx=5)
        tk.Button(frame2, text="هاVLAN وضعیت", command=self.show_vlans, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame2, text="Running نمایش پیکربندی", command=self.show_running_config, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame2, text="Startup نمایش پیکربندی", command=self.show_startup_config, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame2, text="(Ping) تست ارتباط", command=self.ping_ip, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)

        frame3=tk.Frame(self.root)
        frame3.pack(pady=5)
        tk.Button(frame3, text="مشخصات دستگاه", command=self.show_version, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame3, text="نمایش وضعیت منبع تغذیه", command=self.show_power_inline, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame3, text="MAC نمایش جدول", command=self.show_mac_address_table, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame3, text="ARP نمایش جدول", command=self.show_ip_arp, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)
        tk.Button(frame3, text="DHCP مشاهده جدول تخصیص", command=self.show_dhcp_binding, bg="orange", fg="black", width=30, height=2).pack(side=tk.LEFT,padx=5)


        frame4=tk.Frame(self.root)
        frame4.pack(pady=(350,10))
        tk.Button(frame4, text="قطع ارتباط", command=self.disconnect_from_switch, bg="red", fg="white", width=30, height=2).pack(side=tk.LEFT,padx=(20,5))
        tk.Button(frame4, text="ذخیره تنظیمات", command=self.save_running_configuration, bg="red", fg="white", width=30, height=2).pack(side=tk.LEFT,padx=(5,20))
        




    def backup_config(self):
        values=[
            " TFTP Server آدرس : ",
            " نام فایل پشتیبان : "
        ]
        user_inputs= easygui.multenterbox("لطفا مقادیر زیر را وارد کنید ","ورود اطلاعات",values)
        tftp_server_ip , backup_filename = user_inputs
        if tftp_server_ip and backup_filename:
            command = f"copy running-config tftp:\n{tftp_server_ip}\n{backup_filename}\n"
            output = self.connection.send_command_timing(command)
            time.sleep(4)
            self.show_output(output)
            if "!" in output :
                messagebox.showinfo("ذخیره اطلاعات", ".فایل پشتیبان با موفقیت ارسال شد")
            else :
                messagebox.showinfo("ذخیره اطلاعات", ".خود را بررسی کنید TFTP خطایی رخ داده،لطفا سرور")



    def reboot_switch(self):
        confirm = messagebox.askyesno("تایید | انصراف", "آیا مایل هستید که دستگاه را مجددا راه اندازی کنید؟")
        if confirm:
            output = self.connection.send_command_timing(f"reload" , expect_string='confirm')
            messagebox.showinfo("Disconnect", ".دستگاه در حال راه اندازی مجدد میباشد")
            self.connection.disconnect()
            self.create_main_page()



    def ping_ip(self):
        ip_address = simpledialog.askstring("\tورود اطلاعات", "\t\t:مورد نظر را وارد کنید IP آدرس")
        if ip_address:
            output = self.connection.send_command(f"ping {ip_address}")
            time.sleep(4)
            self.show_output(output)
            if "!!!!!" in output :
                messagebox.showinfo("ذخیره اطلاعات", "ارتباط با آدرس"+str(ip_address)+".با موفقیت برقرار شد")
            else :
                messagebox.showinfo("ذخیره اطلاعات", ".خطایی رخ داده ، لطفا ارتباطات خود را بررسی کنید")



    def save_running_configuration(self):
        confirm = messagebox.askyesno("تایید | انصراف", "آیا مایل هستید تنظیمات مورد نظر ذخیره شود؟")
        if confirm:
            cmd = 'write memory'
            if cmd:
                output = self.connection.send_command(cmd)
                time.sleep(4)
                self.show_output(output)
                if "[OK]" in output :
                    messagebox.showinfo("ذخیره اطلاعات", ".تنظیمات مورد نظر با موفقیت ذخیره شد")
                else :
                    messagebox.showinfo("ذخیره اطلاعات", ".خطایی رخ داده ، لطفا مجددا تلاش کیند")



    def shutdown_interface(self):
        interface = simpledialog.askstring("ورود اطلاعات", "\t(GigabitEthernet0/1 مثلاً) :Interface نام")
        if interface:
            commands = [
                f'interface {interface}',
                'shutdown',
            ]
            output = self.connection.send_config_set(commands)
            messagebox.showinfo("خروجی", ".انجام شد، لطفا مجددا وضعیت اینترفیس را بررسی نمایید")




    def no_shutdown_interface(self):
        interface = simpledialog.askstring("ورود اطلاعات", "\t(GigabitEthernet0/1 مثلاً) :Interface نام")
        if interface:
            commands = [
                f'interface {interface}',
                'no shutdown',
            ]
            output = self.connection.send_config_set(commands)
            messagebox.showinfo("خروجی", ".انجام شد، لطفا مجددا وضعیت اینترفیس را بررسی نمایید")


    def add_interface_to_vlan(self):
        values=[
            "\t(GigabitEthernet0/1 مثلاً)Interface نام :",
            "\tVLAN شماره :"
        ]
        user_inputs= easygui.multenterbox("لطفا مقادیر زیر را وارد کنید ","ورود اطلاعات",values)
        interface , vlan_id = user_inputs
        if interface and vlan_id:
            commands = [
                f'configure terminal',
                f'interface {interface}',
                f'switchport mode access',
                f'switchport access vlan {vlan_id}',
            ]
            output = self.connection.send_config_set(commands)
            


    def show_interfaces(self):
        output = self.connection.send_command("show ip interface brief")
        self.show_output(output)



    def show_vlans(self):
        output = self.connection.send_command("show vlan brief")
        self.show_output(output)



    def show_running_config(self):
        output = self.connection.send_command("show running-config")
        self.show_output(output)



    def show_version(self):
        output = self.connection.send_command("show version")
        self.show_output(output)



    def show_power_inline(self):
        output = self.connection.send_command("show power inline")
        self.show_output(output)



    def show_mac_address_table(self):
        output = self.connection.send_command("show mac address-table")
        self.show_output(output)



    def show_ip_arp(self):
        output = self.connection.send_command("show ip arp")
        self.show_output(output)



    def show_dhcp_binding(self):
        output = self.connection.send_command("show ip dhcp binding")
        self.show_output(output)



    def show_startup_config(self):
        output = self.connection.send_command("show startup-config")
        self.show_output(output)



    def disconnect_from_switch(self):
        if self.connection:
            self.connection.disconnect()
            messagebox.showinfo("Disconnect", ".قطع ارتباط با موفقیت انجام شد")
            self.create_main_page()



    def show_output(self, output):
        self.clear_frame()
        tk.Label(self.root, text="خروجی:", font=("Calibri (Body)", 18,"bold")).pack(pady=20)
        output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=25)
        output_text.pack(pady=10)
        output_text.insert(tk.END, output)
        tk.Button(self.root, text="بازگشت به صفحه مدیریت", font=("Calibri (Body)", 14 , "bold"), command=self.create_management_page , bg="orange", fg="black").pack(padx=10,pady=10)



    def show_help(self):
        help_message = """این نرم افزار توسط شرکت فنی و مهندسی دایان تکنولوژی جهت سهولت در مدیریت سوئیچ های شرکت سیسکو طراحی و توسعه داده شده است ، جهت کسب اطلاعات بیشتر با ما در ارتباط باشید www.dayantec.com | 02196625007 | info@dayantec.com"""
        messagebox.showinfo("راهنما", help_message)



    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = CiscoSwitchManager(root)
    root.mainloop()
