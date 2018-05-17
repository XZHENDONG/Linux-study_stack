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
using System.Diagnostics;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

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

        private static string URL =@"http://127.0.0.1:9000";
        private static string httpCmd = @"python ./http_request.py ";
        private static string post = @" --post ";
        private static string get = @" --get ";
        private static string put = @" --put ";
        private static string data = @" --data ";


        private bool Auth(string username,string passwd) {
            Loginjson userinfo = new Loginjson();
            userinfo.account = username;
            userinfo.passwd = passwd;
            userinfo.role = "student";
            string cmd = httpCmd+post+URL+@"/api/v1/login/ "+data+ "\""+JsonConvert.SerializeObject(userinfo).Replace("\"","'") + "\"";
            
            string output="";
            RunCmd(cmd,out output,0);
            output = output.Replace("u'", "'");
            //Responejson respone = JsonConvert.DeserializeObject<Responejson>(output);
            JObject responejson = JObject.Parse(output);
            if ((int)responejson["status"]==1) {
                MessageBox.Show(output);
                Console.WriteLine(output);
                return true;
            }
            return false;
        }

        private static string CmdPath = @"C:\Windows\System32\cmd.exe";

        public static void RunCmd(string cmd, out string output, int asncy)
        {
            cmd = cmd.Trim().TrimEnd('&')+ "&exit";//说明：不管命令是否成功均执行exit命令，否则当调用ReadToEnd()方法时，会处于假死状态
            using (Process p = new Process())
            {
                p.StartInfo.FileName = CmdPath;
                p.StartInfo.UseShellExecute = false;        //是否使用操作系统shell启动
                p.StartInfo.RedirectStandardInput = true;   //接受来自调用程序的输入信息
                p.StartInfo.RedirectStandardOutput = true;  //由调用程序获取输出信息
                p.StartInfo.RedirectStandardError = true;   //重定向标准错误输出
                p.StartInfo.CreateNoWindow = true;          //不显示程序窗口
                p.StartInfo.WorkingDirectory = System.Environment.CurrentDirectory;
                p.Start();//启动程序

                //向cmd窗口写入命令
                p.StandardInput.WriteLine(cmd);
                p.StandardInput.AutoFlush = true;

                //获取cmd窗口的输出信息
                output = "";
                if (asncy == 0)
                {
                    output = p.StandardOutput.ReadToEnd();
                    string[] csvtxt=output.Split('\n');
                    output = csvtxt[csvtxt.Length - 2];
                    p.WaitForExit();//等待程序执行完退出进程
                }
                p.Close();
            }
        }

    }

    class Loginjson {
        public string account;
        public string passwd;
        public string role;
    }
    class Responejson
    {
        public int status;
        public string message;
        public string user_id;
        public string error;
    }
}
