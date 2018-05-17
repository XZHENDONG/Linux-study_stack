using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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
using System.Windows.Threading;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using Microsoft.Scripting.Runtime;
using System.Diagnostics;
using Newtonsoft.Json.Linq;

namespace WpfApp1
{
    public class Person
    {
        
        public int num { get; set; }
        public string title { get; set; }
        public string status { get; set; }

    }
    /// <summary>
    /// student_client.xaml 的交互逻辑
    /// </summary>
    public partial class student_client : Window
    {
        private Person person;
        public Person[] Persons;
        private ScriptEngine pyEngine;
        private int nextpage = 0;
        public student_client()
        {
            InitPerson();
            InitializeComponent();
            string test = "<div class=\"markdown-body editormd-preview-container\" previewcontainer=\"true\" style=\"padding: 20px;\"><h2 id=\"h2-ls-\"><a name=\"ls练习题\" class=\"reference-link\"></a><span class=\"header-link octicon octicon-link\"></span>ls练习题</h2><p>运行ls命令。</p> </div>";
            
            webbrowser.NavigateToString(ConvertExtendedASCII(test));
            datagrid.ItemsSource = this.Persons;
            GetTable();

        }



        public static string ConvertExtendedASCII(string HTML)
        {
            StringBuilder str = new StringBuilder();
            char c;
            for (int i = 0; i < HTML.Length; i++)
            {
                c = HTML[i];
                if (Convert.ToInt32(c) > 127)
                {
                    str.Append("&#" + Convert.ToInt32(c) + ";");
                }
                else
                {
                    str.Append(c);
                }
            }
            return str.ToString();
        }

        private void InitPerson()
        {
            
            this.Persons = new Person[2];
            this.Persons[0] = new Person();
            this.Persons[0].num = 1;
            this.Persons[0].title = "ls练习题";
            this.Persons[0].status = "完成";
            this.Persons[1] = new Person();
            this.Persons[1].num = 2;
            this.Persons[1].title = "cd练习题";
            this.Persons[1].status = "未完成";


        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            string cmd = vmCmd + @" --start ";
            string output = "";
            RunCmd(cmd, out output ,1); 
        }

        private static string CmdPath = @"C:\Windows\System32\cmd.exe";
        private static string URL = @" http://127.0.0.1:9000";
        private static string httpCmd = @"python ./http_request.py ";
        private static string post = @" --post ";
        private static string get = @" --get ";
        private static string put = @" --put ";
        private static string data = @" --data ";
        private static string vmCmd = @"python .\vm_control.py ";

        public static void RunCmd(string cmd, out string output, int asncy)
        {
            cmd = cmd.Trim().TrimEnd('&') + "&exit";//说明：不管命令是否成功均执行exit命令，否则当调用ReadToEnd()方法时，会处于假死状态
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
                if (asncy == 0) {
                    output = p.StandardOutput.ReadToEnd();
                    string[] csvtxt = output.Split('\n');
                    output = csvtxt[csvtxt.Length - 2];
                    p.WaitForExit();//等待程序执行完退出进程
                }   
                p.Close();
            }
        }

        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            string cmd = vmCmd + @" --shutdown ";
            string output = "";
            RunCmd(cmd, out output, 1);
        }

        private void Button_Click_2(object sender, RoutedEventArgs e)
        {
            string cmd = vmCmd + @" --reboot ";
            string output = "";
            RunCmd(cmd, out output, 1);
        }

        private void GetTable()
        {
            string cmd = httpCmd + get + URL + "/api/v1/practices" + data + "table_rows=" + nextpage;
            string output = "";
            RunCmd(cmd, out output, 0);
            output = output.Replace("u'", "'");
            JObject responejson= JObject.Parse(output);
            MessageBox.Show(output);

        }
    }



    
}
