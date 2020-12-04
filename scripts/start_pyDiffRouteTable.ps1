##----------------------------------------------------------------------------##
## Main function.
##----------------------------------------------------------------------------##
function Main()
{
    $CMD1 = "./dist/pyDiffRouteTable.exe"
    $CMD2 = "./pyDiffRouteTable.exe"

    if (Test-Path $CMD1) {
        $CMD = $CMD1
    }
    elseif (Test-Path $CMD2) {
        $CMD = $CMD2
    }
    else {
        $CMD = SelectFile "pyDiffRouteTable.exeを選択してください。"
    }

    if ($NULL -eq $CMD) {
        return
    }

    $DEST_DIR = SelectFolder("RouteTableの保存先ディレクトリを選択してください。")
    if ($NULL -eq $DEST_DIR) {
        return
    }

    $CMDLINE = "$CMD $DEST_DIR"

    Add-Type -Assembly System.Windows.Forms
    $res = [System.Windows.Forms.MessageBox]::Show("$CMDLINE`n`n実行しますか？", "実行確認", "YesNo", "Question")
    if ($res -eq "Yes") {
        Invoke-Expression $CMDLINE
    }
}

##----------------------------------------------------------------------------##
## Display Select EXE File Dialog.
##----------------------------------------------------------------------------##
function SelectFile([string]$message)
{
    [void][System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")

    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Filter = "EXEファイル(*.EXE)|*.EXE;"
    $dialog.InitialDirectory = Get-Location
    $dialog.Title = $message

    if($dialog.ShowDialog() -eq "OK") {
        return $dialog.FileName
    }
    else {
        return $NULL
    }
}

##----------------------------------------------------------------------------##
## Display Select Folder Dialog.
##----------------------------------------------------------------------------##
function SelectFolder($message)
{
    [void][System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms")

    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.SelectedPath = Get-Location
    $dialog.Description = $message

    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
       return $dialog.SelectedPath
    }
    else {
        return $NULL
    }
}

##----------------------------------------------------------------------------##
## Call Main function.
##----------------------------------------------------------------------------##

Main
