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
using Newtonsoft.Json;

namespace WpfApp1
{
    public class Exerc
    {
        
        public int exerc_id { get; set; }
        public string exerc_markdown { get; set; }
        public string exerc_html { get; set; }
        public string status { get; set; }

    }

    public class ExercRow {
        public int num { get; set; }
        public int exerc_id { get; set; }
        public string title { get; set; }
        public string status { get; set; }
    }
    /// <summary>
    /// student_client.xaml 的交互逻辑
    /// </summary>
    public partial class Student_client : Window
    {
        
        public ExercRow[] exercs;
        private int nextpage = 0;
        private bool has_next = true;
        private Exerc[] exerc_list;
        public int userID=1;
        public Student_client()
        {
            InitializeComponent();
            GetTable();
            datagrid.ItemsSource = this.exercs;
            string test = exerc_list[0].exerc_html;
            webbrowser.NavigateToString(ConvertExtendedASCII(test));
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
        private void title_Button_Click(object sender, RoutedEventArgs e)
        {
            ExercRow tableList = ((Button)sender).DataContext as ExercRow;
            MessageBox.Show(tableList.exerc_id.ToString());
        }

        private void GetTable()
        {
            string cmd = httpCmd + get + URL + "/api/v1/practices" + data + "{'table_rows':" + nextpage+"}";
            string output = "";
            RunCmd(cmd, out output, 0);
            output = output.Replace("u'", "'").Replace("'next': False", "'next': false").Replace("'next': True", "'next': true");
            JObject responejson= JObject.Parse(output);
            nextpage = (int)responejson["next_page"];
            has_next = responejson["next"].Value<bool>();
            JArray exerc_arry = JArray.Parse(responejson["exerc"].ToString());
            this.exerc_list = new Exerc[exerc_arry.Count];
            this.exercs = new ExercRow[exerc_arry.Count];


            for (int i = 0; i < exerc_arry.Count; i++)
            {
                this.exerc_list[i] = JsonConvert.DeserializeObject<Exerc>(exerc_arry[i].ToString());
                this.exercs[i] = new ExercRow();
                this.exercs[i].num = i+1;
                this.exercs[i].exerc_id = exerc_list[i].exerc_id;
                this.exercs[i].title = exerc_list[i].exerc_markdown.Split('\n')[0].Trim('#');
                cmd = httpCmd + get + URL + "/api/v1/checkerresult" + data + "{'userID':" + this.userID + @",'exercID':" + exerc_list[i].exerc_id + "}";
                output = "";
                RunCmd(cmd, out output, 0);
                output = output.Replace("u'", "'");
                responejson = JObject.Parse(output);
                exercs[i].status = responejson["message"].Value<string>();
            }
        }


    }



    
}
