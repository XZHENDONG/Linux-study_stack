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

namespace WpfApp1
{
    public class Person
    {
        public string Name { get; set; }
        public int Age { get; set; }
    }
    /// <summary>
    /// student_client.xaml 的交互逻辑
    /// </summary>
    public partial class student_client : Window
    {
        private Person person;
        public Person[] Persons;
        public student_client()
        {
            InitPerson();
            InitializeComponent();
            DispatcherTimer dispatcherTimer = new DispatcherTimer();
            dispatcherTimer.Tick += new EventHandler(dispatcherTimer_Tick);
            dispatcherTimer.Interval = new TimeSpan(0, 0, 1);
            dispatcherTimer.Start();
            datagrid.ItemsSource = this.Persons;
        }

        private void InitPerson()
        {
            
            this.Persons = new Person[1];
            this.Persons[0] = new Person();
            this.Persons[0].Name = "tom";
            this.Persons[0].Age = 16;
            

        }

        private void dispatcherTimer_Tick(object sender, EventArgs e)
        {
            // Updating the Label which displays the current second
            timers.Content = DateTime.Now.TimeOfDay;

            // Forcing the CommandManager to raise the RequerySuggested event
            CommandManager.InvalidateRequerySuggested();
        }
    }


    
}
