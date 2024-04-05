var elements = document.querySelectorAll('div[class*="video-card-info"]');

let current_ele=null
for (var i = 0; i < elements.length; i++) {
    var element = elements[i];
    text=element.querySelector('div[class*=info-title-text]').innerText
    if(text.includes('龙珠')){
        current_ele=element
        break
    }
}

if(current_ele==null){
    throw "未找到当前稿件"
}

cli=current_ele.querySelector('div[class*=ghost-btn]')
cli.click()

// 点击替换
document.querySelector("#dialog-1").querySelector('div[class*=btn]>span').click()

// 点击选择上传页
document.querySelector("#dialog-2").querySelectorAll('div[class*=tabItem]')[1].click()

// 最终触发上传
document.querySelector('div[class="semi-upload-drag-area"]').click()
