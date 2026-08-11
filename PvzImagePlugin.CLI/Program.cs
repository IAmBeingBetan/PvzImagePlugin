using System;
using System.Diagnostics;
using System.IO;

namespace PvzImagePlugin.CLI
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("用法:");
                Console.WriteLine("  train   <数据集目录>");
                Console.WriteLine("  predict <图片路径>");
                return;
            }

            string mode = args[0];

            // Python 路径（按你机器实际情况确认）
            string pythonExe = @"D:\Python39_64\Python39_64\python.exe";

            // 修正上一轮的语法错误：删掉 s，正确拼接路径
            string pythonDir = Path.GetFullPath(
                Path.Combine(
                    AppDomain.CurrentDomain.BaseDirectory,
                    @"..\..\..\PvzImagePlugin.ML"
                )
            );

            // 调试输出，方便确认路径是否正确
            Console.WriteLine("Python 路径: " + pythonExe);
            Console.WriteLine("工作目录: " + pythonDir);

            switch (mode)
            {
                case "train":
                    if (args.Length < 2)
                    {
                        Console.WriteLine("缺少数据集目录");
                        return;
                    }
                    RunPython(pythonExe, pythonDir, "train.py", args[1]);
                    break;

                case "predict":
                    if (args.Length < 2)
                    {
                        Console.WriteLine("缺少图片路径");
                        return;
                    }
                    RunPython(pythonExe, pythonDir, "predict.py", args[1]);
                    break;

                default:
                    Console.WriteLine("未知模式: " + mode);
                    break;
            }
        }

        static void RunPython(string pythonExe, string workingDir, string script, string arg)
        {
            var psi = new ProcessStartInfo
            {
                FileName = pythonExe,
                Arguments = $"\"{script}\" \"{arg}\"",
                WorkingDirectory = workingDir,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var proc = Process.Start(psi);
            if (proc == null)
            {
                Console.WriteLine("无法启动 Python 进程");
                return;
            }

            string output = proc.StandardOutput.ReadToEnd();
            string error = proc.StandardError.ReadToEnd();
            proc.WaitForExit();

            if (!string.IsNullOrWhiteSpace(output))
            {
                Console.WriteLine(output);
            }

            if (!string.IsNullOrWhiteSpace(error))
            {
                Console.WriteLine("PYTHON ERROR:");
                Console.WriteLine(error);
            }
        }
    }
}