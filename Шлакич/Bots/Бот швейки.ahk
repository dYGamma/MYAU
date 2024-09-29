Toggle := False
StepCheck := 1
Check := true

FX1 := 0
FY1 := 0
FX2 := 0
FY2 := 0
FX3 := 0
FY3 := 0
FX4 := 0
FY4 := 0
FX5 := 0
FY5 := 0
FX6 := 0
FY6 := 0
FX7 := 0
FY7 := 0
FX8 := 0
FY8 := 0
FX9 := 0
FY9 := 0
FX10 := 0
FY10 := 0
FX11 := 0
FY11 := 0
FX12 := 0
FY12 := 0
FX13 := 0
FY13 := 0
FX14 := 0
FY14 := 0
FX15 := 0
FY15 := 0
FX16 := 0
FY16 := 0
FX17 := 0
FY17 := 0
FX18 := 0
FY18 := 0
FX19 := 0
FY19 := 0
FX20 := 0
FY20 := 0

#MaxThreadsPerHotkey 2

F3::
    Toggle := !Toggle
    Check := true
    StepCheck := 1
    loop {
        If not Toggle
        break
        1:
        Sleep, 100
        if(Check)
        {
            if(StepCheck == 1)
            {
                ImageSearch, FXx1, FYy1, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_0.jpg
                if(ErrorLevel = 0)
                {
                    FX1 := % FXx1 + 20
                    FY1 := % FYy1 + 20
                    StepCheck := 2
                }
            }
            if(StepCheck == 2)
            {
                ImageSearch, FXx2, FYy2, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_1.jpg
                if(ErrorLevel = 0)
                {
                    FX2 := % FXx2 + 20
                    FY2 := % FYy2 + 20
                    StepCheck := 3
                }
            }
            if(StepCheck == 3)
            {
                ImageSearch, FXx3, FYy3, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_2.jpg
                if(ErrorLevel = 0)
                {
                    FX3 := % FXx3 + 20
                    FY3 := % FYy3 + 20
                    StepCheck := 4
                }
            }
            if(StepCheck == 4)
            {
                ImageSearch, FXx4, FYy4, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_3.jpg
                if(ErrorLevel = 0)
                {
                    FX4 := % FXx4 + 20
                    FY4 := % FYy4 + 20
                    StepCheck := 5
                }
            }
            if(StepCheck == 5)
            {
                ImageSearch, FXx5, FYy5, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_4.jpg
                if(ErrorLevel = 0)
                {
                    FX5 := % FXx5 + 20
                    FY5 := % FYy5 + 20
                    StepCheck := 6
                }
            }
            if(StepCheck == 6)
            {
                ImageSearch, FXx6, FYy6, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_5.jpg
                if(ErrorLevel = 0)
                {
                    FX6 := % FXx6 + 20
                    FY6 := % FYy6 + 20
                    StepCheck := 7
                }
            }
            if(StepCheck == 7)
            {
                ImageSearch, FXx7, FYy7, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_6.jpg
                if(ErrorLevel = 0)
                {
                    FX7 := % FXx7 + 20
                    FY7 := % FYy7 + 20
                    StepCheck := 8
                }
            }
            if(StepCheck == 8)
            {
                ImageSearch, FXx8, FYy8, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_7.jpg
                if(ErrorLevel = 0)
                {
                    FX8 := % FXx8 + 20
                    FY8 := % FYy8 + 20
                    StepCheck := 9
                }
            }
            if(StepCheck == 9)
            {
                ImageSearch, FXx9, FYy9, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_8.jpg
                if(ErrorLevel = 0)
                {
                    FX9 := % FXx9 + 20
                    FY9 := % FYy9 + 20
                    StepCheck := 10
                }
            }
            if(StepCheck == 10)
            {
                ImageSearch, FXx10, FYy10, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_9.jpg
                if(ErrorLevel = 0)
                {
                    FX10 := % FXx10 + 20
                    FY10 := % FYy10 + 20
                    StepCheck := 11
                }
            }

            if(StepCheck == 11)
            {
                ImageSearch, FXx11, FYy11, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_10.jpg
                if(ErrorLevel = 0)
                {
                    FX11 := % FXx11 + 20
                    FY11 := % FYy11 + 20
                    StepCheck := 12
                }
            }
            if(StepCheck == 12)
            {
                ImageSearch, FXx12, FYy12, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_11.jpg
                if(ErrorLevel = 0)
                {
                    FX12 := % FXx12 + 20
                    FY12 := % FYy12 + 20
                    StepCheck := 13
                }
            }
            if(StepCheck == 13)
            {
                ImageSearch, FXx13, FYy13, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_12.jpg
                if(ErrorLevel = 0)
                {
                    FX13 := % FXx13 + 20
                    FY13 := % FYy13 + 20
                    StepCheck := 14
                }
            }
            if(StepCheck == 14)
            {
                ImageSearch, FXx14, FYy14, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_13.jpg
                if(ErrorLevel = 0)
                {
                    FX14 := % FXx14 + 20
                    FY14 := % FYy14 + 20
                    StepCheck := 15
                }
            }
            if(StepCheck == 15)
            {
                ImageSearch, FXx15, FYy15, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_14.jpg
                if(ErrorLevel = 0)
                {
                    FX15 := % FXx15 + 20
                    FY15 := % FYy15 + 20
                    StepCheck := 16
                }
            }
            if(StepCheck == 16)
            {
                ImageSearch, FXx16, FYy16, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_15.jpg
                if(ErrorLevel = 0)
                {
                    FX16 := % FXx16 + 20
                    FY16 := % FYy16 + 20
                    StepCheck := 17
                }
            }
            if(StepCheck == 17)
            {
                ImageSearch, FXx17, FYy17, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_16.jpg
                if(ErrorLevel = 0)
                {
                    FX17 := % FXx17 + 20
                    FY17 := % FYy17 + 20
                    StepCheck := 18
                }
            }
            if(StepCheck == 18)
            {
                ImageSearch, FXx18, FYy18, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_17.jpg
                if(ErrorLevel = 0)
                {
                    FX18 := % FXx18 + 20
                    FY18 := % FYy18 + 20
                    StepCheck := 19
                }
            }
            if(StepCheck == 19)
            {
                ImageSearch, FXx19, FYy19, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_18.jpg
                if(ErrorLevel = 0)
                {
                    FX19 := % FXx19 + 20
                    FY19 := % FYy19 + 20
                    StepCheck := 20
                }
            }
            if(StepCheck == 20)
            {
                ImageSearch, FXx20, FYy20, 770, 280, 1144, 805, *50 %A_ScriptDir%\img\number_19.jpg
                if(ErrorLevel = 0)
                {
                    FX20 := % FXx20 + 20
                    FY20 := % FYy20 + 20
                    Check := False
                    StepCheck := 1
                    Goto, 1
                }
            }
        }
        else
        {
            if(StepCheck == 1)
            {
                CLick, %FX1%, %FY1%
                Sleep, 1000
                StepCheck := 2
                Goto, 1
            }
            if(StepCheck == 2)
            {
                CLick, %FX2%, %FY2%
                Sleep, 1000
                Click
                StepCheck := 3
                Goto, 1
            }
            if(StepCheck == 3)
            {
                CLick, %FX3%, %FY3%
                Sleep, 1000
                Click
                StepCheck := 4
                Goto, 1
            }
            if(StepCheck == 4)
            {
                CLick, %FX4%, %FY4%
                Sleep, 1000
                CLick
                StepCheck := 5
                Goto, 1
            }
            if(StepCheck == 5)
            {
                CLick, %FX5%, %FY5%
                Sleep, 1000
                CLick
                StepCheck := 6
                Goto, 1
            }
            if(StepCheck == 6)
            {
                CLick, %FX6%, %FY6%
                Sleep, 1000
                CLick
                StepCheck := 7
                Goto, 1
            }
            if(StepCheck == 7)
            {
                CLick, %FX7%, %FY7%
                Sleep, 1000
                CLick
                StepCheck := 8
                Goto, 1
            }
            if(StepCheck == 8)
            {
                CLick, %FX8%, %FY8%
                Sleep, 1000
                CLick
                StepCheck := 9
                Goto, 1
            }
            if(StepCheck == 9)
            {
                CLick, %FX9%, %FY9%
                Sleep, 1000
                CLick
                StepCheck := 10
                Goto, 1
            }
            if(StepCheck == 10)
            {
                CLick, %FX10%, %FY10%
                Sleep, 1000
                CLick
                StepCheck := 11
                Goto, 1
            }
            if(StepCheck == 11)
            {
                CLick, %FX11%, %FY11%
                Sleep, 1000
                CLick
                StepCheck := 12
                Goto, 1
            }
            if(StepCheck == 12)
            {
                CLick, %FX12%, %FY12%
                Sleep, 1000
                CLick
                StepCheck := 13
                Goto, 1
            }
            if(StepCheck == 13)
            {
                CLick, %FX13%, %FY13%
                Sleep, 1000
                CLick
                StepCheck := 14
                Goto, 1
            }
            if(StepCheck == 14)
            {
                CLick, %FX14%, %FY14%
                Sleep, 1000
                CLick
                StepCheck := 15
                Goto, 1
            }
            if(StepCheck == 15)
            {
                CLick, %FX15%, %FY15%
                Sleep, 1000
                CLick
                StepCheck := 16
                Goto, 1
            }
            if(StepCheck == 16)
            {
                CLick, %FX16%, %FY16%
                Sleep, 1000
                CLick
                StepCheck := 17
                Goto, 1
            }
            if(StepCheck == 17)
            {
                CLick, %FX17%, %FY17%
                Sleep, 1000
                CLick
                StepCheck := 18
                Goto, 1
            }
            if(StepCheck == 18)
            {
                CLick, %FX18%, %FY18%
                Sleep, 1000
                CLick
                StepCheck := 19
                Goto, 1
            }
            if(StepCheck == 19)
            {
                CLick, %FX19%, %FY19%
                Sleep, 1000
                CLick
                StepCheck := 20
                Goto, 1
            }
            if(StepCheck == 20)
            {
                CLick, %FX20%, %FY20%
                Sleep, 1000
                CLick
                Check := true
                StepCheck := 1
                Goto, 1
            }
        }
    }
return
