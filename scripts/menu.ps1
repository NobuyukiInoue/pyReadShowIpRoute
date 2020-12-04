# アセンブリのロード
Add-Type -AssemblyName System.Windows.Forms

function Main($logPath) {
    if (-Not(Test-Path $logPath)) {
        mkdir "./temp"
    }
    
    $form = CreateForm $logPath

    # フォームの表示
    $form.Showdialog()
}

function CreateForm($logPath) {
    # フォーム
    $form = New-Object System.Windows.Forms.Form
    $form.Size = "350,220"
    $form.Startposition = "centerscreen"
    $form.Text = "pyReadShowIpRouteスクリプト群操作メニュ"
    $form.MaximizeBox = $FALSE
    $form.MinimizeBox = $FALSE

    # ボタン1
    $Button1 = New-Object System.Windows.Forms.Button
    $Button1.Location = "40, 40"
    $Button1.Size = "240, 45"
    $Button1.Text = "logファイル群からRouteTable群を生成する"
    $Button1.FlatStyle = "popup"

    # ボタン2
    $Button2 = New-Object System.Windows.Forms.Button
    $Button2.Location = "40, 90"
    $Button2.Size = "240, 45"
    $Button2.Text = "RouteTable群の中から`n直近の２つのファイルのDiffを出力する"
    $Button2.FlatStyle = "popup"

    # ラベル
    $Label1 = New-Object System.Windows.Forms.Label
    $Label1.Location = "40, 150"
    $Label1.Size = "240, 45"
    $Label1.Text = ""
    $Label1.ForeColor = "#FF0000"

    # メニューバー
    $Menu = New-Object System.Windows.Forms.MenuStrip

    # 項目1
    $Item1 = New-Object System.Windows.Forms.ToolStripMenuItem
    $Item1.Text = "help"

    # 項目1 - 子項目1
    $SubMenu1 = New-Object System.Windows.Forms.ToolStripMenuItem
    $SubMenu1.Text = "Software Information"
    
    # ショートカットキー Ctrl+V
    $SubMenu1.ShortcutKeys = [System.Windows.Forms.Keys]::Control, [System.Windows.Forms.Keys]::V

    $Click01 = {
        # フォーム - ソフトウェア情報
        $form20 = New-Object System.Windows.Forms.Form
        $form20.Size = "350, 160"
        $form20.Startposition = "centerscreen"
        $form20.Text = "ソフトウェア情報"
        $form20.MaximizeBox = $FALSE
        $form20.MinimizeBox = $FALSE

        # ラベル
        $Label21 = New-Object System.Windows.Forms.Label
        $Label21.Location = "10, 10"
        $Label21.AutoSize = $TRUE
        $Label21.Text = "pyReadShowIpRoute`n`nCopyright (c) 2020 Nobuyuki Inoue`n`nURL)"

        # ラベル
        $LinkLabel22 = New-Object System.Windows.Forms.LinkLabel
        $LinkLabel22.Location = "10, 80"
        $LinkLabel22.AutoSize = $TRUE
        $LinkLabel22.Text = "https://github.com/NobuyukiInoue/pyReadShowIpRoute"

        # リンクラベルのクリックイベント
        $Link = {
            $IE = New-Object -ComObject InternetExplorer.Application
            $IE.Navigate("https://github.com/NobuyukiInoue/pyReadShowIpRoute")
            $IE.Visible = $True
        }
        $LinkLabel22.Add_Click($Link)

        $form20.Controls.Add($Label21)
        $form20.Controls.Add($LinkLabel22)

        $form20.Showdialog()
    }
    $SubMenu1.Add_Click($Click01)

    $Item1.DropDownItems.AddRange(@($SubMenu1))
    $Menu.Items.AddRange(@($Item1))

    $form.Controls.Add($Button1)
    $form.Controls.Add($Button2)
    $form.Controls.Add($Label1)

    # メニューバーに項目1・項目2を入れる
    $form.Controls.AddRange(@($Menu))

    # ボタン1のクリックイベント
    $Button1.Add_Click({
        # $Label1.Text = "処理中..."
        $this.Parent.Controls[2].Text = "pyAutoReadShowIpRoute処理中..."
        $this.Enabled = $FALSE

        $TimeStamp = Get-Date -Format "yyyyMMdd_hhmmss"
        $tempFilePath = "$logPath/pyAutoReadShowIpRoute_$TimeStamp.log"
        Invoke-Expression "./scripts/start_pyAutoReadShowIpRoute.ps1" | Out-File -Encoding default $tempFilePath

        # $Label1.Text = ""
        $this.Parent.Controls[2].Text = ""
        $this.Enabled = $TRUE

        if ((Get-ChildItem $tempFilePath).Length -eq 0) {
            Remove-Item $tempFilePath
        }
        else {
            Invoke-Item $tempFilePath
        }
    })

    # ボタン2のクリックイベント
    $Button2.Add_Click({
        # $Label1.Text = "処理中..."
        $this.Parent.Controls[2].Text = "pyDiffRouteTable処理中..."
        $this.Enabled = $FALSE

        $TimeStamp = Get-Date -Format "yyyyMMdd_hhmmss"
        $tempFilePath = "$logPath/pyDiffRouteTable_$TimeStamp.log"
        Invoke-Expression "./scripts/start_pyDiffRouteTable.ps1" | Out-File -Encoding default $tempFilePath

        # $Label1.Text = ""
        $this.Parent.Controls[2].Text = ""
        $this.Enabled = $TRUE

        if ((Get-ChildItem $tempFilePath).Length -eq 0) {
            Remove-Item $tempFilePath
        }
        else {
            Invoke-Item $tempFilePath
        }
    })

    return $form
}

Main "./temp"
