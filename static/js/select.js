// ①Django側にPOST送信する際に記述する"お決まりのコード"
const getCookie = (name) => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
};
const csrftoken = getCookie('csrftoken');

// ②選択されたセレクトメニュー情報をDjango側にPOST送信してデータを取得する
// セレクトメニュー内の要素を取得する
const yearValue = document.getElementById('year_pulldown');
// セレクトメニューの値が変更された時に実行される処理
yearValue.addEventListener('change', (event) => {
  // セレクトメニュー内で選択された値の順番を取得する
  const yearValueId = yearValue.selectedIndex;
  // セレクトメニュー内で選択された値のidを取得する
  const selectedYear = yearValue[yearValueId].value;
  // セレクトメニュー内の要素を取得する
  const monthValue = document.getElementById('month_pulldown');
  const monthValueId = monthValue.selectedIndex;
  const selectedMonth = monthValue[monthValueId].value;
  // 非同期処理を記述する
  async function menu_list() {
    const url = '/pulldown_access/';
    let res = await fetch(url, {
      method: 'POST',
      headers: {
	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'X-CSRFToken': csrftoken,
      },
      // str型で取得してしまう
      body: `year_val=${selectedYear},${selectedMonth}`
    });
    let json = await res.json();
    let query_list = json.query_list;
    let table_body = document.getElementById('table-body');
    table_body.innerHTML = '';
    for (let query of query_list) {
      let tr_block = document.createElement('tr');
      let td_block_1 = document.createElement('td');
      let td_block_2 = document.createElement('td');
      let td_block_3 = document.createElement('td');
      //product_box.className = "product-box";
      //product_txt_box.className = "product-txt-box";
      td_block_1.innerHTML = `${query.reserve_date}`;
      td_block_2.innerHTML = `${query.reserve_time}`;
      td_block_3.innerHTML = `${query.name} ${query.reserve_num}人<br>${query.email}<br>${query.tel}<br>${query.comment}`;
      tr_block.appendChild(td_block_1);
      tr_block.appendChild(td_block_2);
      tr_block.appendChild(td_block_3);
      table_body.appendChild(tr_block);
    }
  }
  // 定義した関数を実行する
  menu_list();
});

// ②選択されたセレクトメニュー情報をDjango側にPOST送信してデータを取得する
// セレクトメニュー内の要素を取得する
const monthValue = document.getElementById('month_pulldown');
// セレクトメニューの値が変更された時に実行される処理
monthValue.addEventListener('change', (event) => {
  // セレクトメニュー内で選択された値の順番を取得する
  const monthValueId = monthValue.selectedIndex;
  // セレクトメニュー内で選択された値のidを取得する
  const selectedMonth = monthValue[monthValueId].value;
  // セレクトメニュー内の要素を取得する
  const yearValue = document.getElementById('year_pulldown');
  const yearValueId = yearValue.selectedIndex;
  const selectedYear = yearValue[yearValueId].value;
  // 非同期処理を記述する
  async function menu_list() {
    const url = '/pulldown_access/';
    let res = await fetch(url, {
      method: 'POST',
      headers: {
	'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'X-CSRFToken': csrftoken,
      },
      // str型で取得してしまう
      body: `year_val=${selectedYear},${selectedMonth}`
    });
    let json = await res.json();
    let query_list = json.query_list;
    let table_body = document.getElementById('table-body');
    table_body.innerHTML = '';
    for (let query of query_list) {
      let tr_block = document.createElement('tr');
      let td_block_1 = document.createElement('td');
      let td_block_2 = document.createElement('td');
      let td_block_3 = document.createElement('td');
      //product_box.className = "product-box";
      //product_txt_box.className = "product-txt-box";
      td_block_1.innerHTML = `${query.reserve_date}`;
      td_block_2.innerHTML = `${query.reserve_time}`;
      td_block_3.innerHTML = `${query.name} ${query.reserve_num}人<br>${query.email}<br>${query.tel}<br>${query.comment}`;
      tr_block.appendChild(td_block_1);
      tr_block.appendChild(td_block_2);
      tr_block.appendChild(td_block_3);
      table_body.appendChild(tr_block);
    }
  }
  // 定義した関数を実行する
  menu_list();
});
