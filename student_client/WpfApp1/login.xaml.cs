using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace WpfApp1
{
    /// <summary>
    /// login.xaml 的交互逻辑
    /// </summary>
    public partial class login : Window
    {
        public login()
        {
            InitializeComponent();
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            if (register_button.Content.Equals("注册"))
            {
                comfirm_label.Visibility = System.Windows.Visibility.Visible;
                comfirm_passwd.Visibility = System.Windows.Visibility.Visible;
                username_label.Visibility = System.Windows.Visibility.Visible;
                username_textbox.Visibility = System.Windows.Visibility.Visible;
                login_button.Content = "提交";
                register_button.Content = "返回";
            }                          
            else if (register_button.Content.Equals("返回"))
            {
                comfirm_label.Visibility = System.Windows.Visibility.Hidden;
                comfirm_passwd.Visibility = System.Windows.Visibility.Hidden;
                username_label.Visibility = System.Windows.Visibility.Hidden;
                username_textbox.Visibility = System.Windows.Visibility.Hidden;
                login_button.Content = "登陆";
                register_button.Content = "注册";
            }
        }

        private void login_button_Click(object sender, RoutedEventArgs e)
        {
            string account=account_text.Text;
            string passwd = passwd_text.Password; 
            if (Auth(account, passwd))
            {
                student_client student_Client = new student_client();
                student_Client.Show();
                this.Close();
            }
            
        }

        private bool Auth(string username,string passwd) {
            return true;
        }

    }
}
