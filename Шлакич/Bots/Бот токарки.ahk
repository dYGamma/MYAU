Toggle := False
#MaxThreadsPerHotkey 2

F3::
    Toggle := !Toggle
    loop {
        If not Toggle
        break
            ImageSearch, FoundX, FoundY, 657, 670 , 1260, 977, *50 %A_ScriptDir%\img\palka.jpg
            if(ErrorLevel = 0)
            {
                FX := % FoundX + 20
                FY := % FoundY + 50
                MouseMove, %FX%, %FY%, 0
            }
    }
return
