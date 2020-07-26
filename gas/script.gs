// config
var spreadsheetId = "<スプレッドシートのURL>";
var lab_name = "<研究室の名前>";

var ss = SpreadsheetApp.openById(spreadsheetId);

// POSTが来ると実行される
function doPost(e) {
  var params = JSON.parse(e.postData.getDataAsString());
  var student_number = params.data;
  decideEditOrAppend(student_number);
  return ContentService.createTextOutput('success');
}

// データを作るか追記するかの判断
function decideEditOrAppend(student_number) {
  const sheet = openMonthlySheet();
  const date = new TimeStatus();
  const data_exist_line = searchDataExist(sheet, date, student_number);
  if (data_exist_line) {
    // データが存在すれば退室時間を書く
    editData(sheet, data_exist_line, date);
  } else {
    // データが存在しなければ新たにデータを入れる
    const data = createAppendData(date, student_number);
    appendData(data, sheet);
  }
  return;
}

// スプレッドシートの最後にデータを追記
function appendData(data, sheet){
  sheet.appendRow(data);
  return;
}

// シートに入力するデータの作成
function createAppendData(date, student_number) {
  const name = getNameFromSheet(student_number);
  return [date.day, student_number, name, lab_name, date.time];
}

// すでにシートにあるなら帰宅時間を追記
function editData(sheet, line, date_now) {
  // getRangeを用いる際、セル番号は1から値がはじまる
  sheet.getRange(line + 1, 6).setValue(date_now.time);
  return;
}

// データの検索
// 入力: 今日の日付、学籍番号
// 出力:
//   - すでにデータがあればカラムを返す
//   - データがなければNULL
function searchDataExist(sheet, date_now, student_id) {
  const data_from_sheet = sheet.getDataRange().getValues();

  // シートの中から日付と学籍番号が一致するものを検索
  for (var i = 1; i < data_from_sheet.length; i++) {
    const line_date = new Date(data_from_sheet[i][0]);
    if (data_from_sheet[i][1] == student_id && 
        line_date.getDate() == date_now.date.getDate() &&
        line_date.getMonth() == date_now.date.getMonth()) {
      return i;
    }
  }
  return null;
}

/// 学籍番号から名前を返す
/// いなければunknownさんにする
function getNameFromSheet(id) {
  // 名前一覧を全部取ってくる
  const nameList = ss.getSheetByName("NameList").getDataRange().getValues();

  for (var i = 1; i < nameList.length; i++) {
    if (nameList[i][0] == id) {
      return nameList[i][1];
    }
  }
  return "unknown";
}

// 今月のシートを開く、なければ新たに開いてSheetを返す
// 入力: シート名
// 出力: シート
function openMonthlySheet() {
  var day = new TimeStatus();
  var yymm = day.yymm;
  var sheet = ss.getSheetByName(yymm);
  if(!sheet) {
    sheet = ss.insertSheet(yymm);
    ss.appendRow(["月／日 MM/DD", "学生証番号 / Student ID", "氏名 / Name", "場所 / Venue", "入室時間 / Entry time", "退室時間 / Exit time"]);
  }
  return sheet;
}

// 日付のフォーマット
TimeStatus = function() {
  this.date = new Date();
  this.yymm = Utilities.formatDate(this.date, 'Asia/Tokyo', 'yyyyMM');
  this.day = Utilities.formatDate(this.date, 'Asia/Tokyo', 'yyyy/MM/dd');
  this.time = Utilities.formatDate(this.date, 'Asia/Tokyo', 'HH:mm');
}
