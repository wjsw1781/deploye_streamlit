window.onload = () => {

    // z-index  目前三层    1000 999 auto 


    // 填写视频尺寸功能
    function fill_video_size(x, y) {
        let all_top_butoome_left_right = Array.from(document.querySelector('#video_size').querySelectorAll('input'))
        let now_ele = all_top_butoome_left_right.filter((item, index) => item.checked == true)

        if (now_ele.length == 0) {
            return
        }

        let now_index = all_top_butoome_left_right.indexOf(now_ele[0])
        if (now_index == all_top_butoome_left_right.length - 1) {
            return
        }
        let all_top_butoome_top_bottom_res = Array.from(document.querySelector('#video_size_res').querySelectorAll('textarea'))

        let old_value = all_top_butoome_top_bottom_res[now_index].value
        let new_value = x + 'x' + y
        all_top_butoome_top_bottom_res[now_index].value = new_value
        // m模拟触发 
        all_top_butoome_top_bottom_res[now_index].dispatchEvent(new Event('input', { bubbles: true }));

        console.log("🚀 ~ fill_video_size ~ value:", new_value)


    }

    //填写水印下边距
    function fill_watermark_bottom(x, y) {


        let shuiyin_open_ele = Array.from(document.querySelector('#is_draw_shuiyin_area').querySelectorAll('input'))
        let now_ele = shuiyin_open_ele.filter((item, index) => item.checked == true)

        if (now_ele.length == 0) {
            return
        }

        let now_index = shuiyin_open_ele.indexOf(now_ele[0])
        if (now_index == shuiyin_open_ele.length - 1) {
            return
        }

        let is_draw_shuiyin_area_res_ele = document.querySelector("#is_draw_shuiyin_area_res").querySelectorAll('textarea')

        let old_value = is_draw_shuiyin_area_res_ele[now_index].value
        let new_value = x + 'x' + y

        is_draw_shuiyin_area_res_ele[now_index].value = new_value
        is_draw_shuiyin_area_res_ele[now_index].dispatchEvent(new Event('input', { bubbles: true }));

        console.log("🚀 ~ fill_watermark_bottom ~ value:", new_value)

    }



    // 全局开关显示鼠标///////////////////////////////////////
    window.is_draw_line = document.querySelector("#is_draw_line").querySelector('input')


    // 移动鼠标显示/////////////////////////////////////////
    window.xy_mousemove = document.createElement('div');
    xy_mousemove.style.position = 'absolute';
    xy_mousemove.style.top = '0';
    xy_mousemove.style.left = '0';
    xy_mousemove.style.width = '100%';
    xy_mousemove.style.height = '100%';
    document.body.appendChild(xy_mousemove);
    document.addEventListener('mousemove', function (event) {

        if (!is_draw_line.checked) {
            // 表明这里要开始标注了 页面上的所有不能被点击  
            xy_mousemove.style.zIndex = '-1';

        } else {
            xy_mousemove.style.zIndex = '999';

        }


        var x = event.clientX;
        var y = event.clientY;

        var verticalLine = document.createElement('div');
        verticalLine.style.position = 'absolute';
        verticalLine.style.left = x + 'px';
        verticalLine.style.width = '1px';
        verticalLine.style.height = '100%';
        verticalLine.style.backgroundColor = 'red';

        // 创建水平线条
        var horizontalLine = document.createElement('div');
        horizontalLine.style.position = 'absolute';
        horizontalLine.style.top = y + 'px';
        horizontalLine.style.width = '100%';
        horizontalLine.style.height = '1px';
        horizontalLine.style.backgroundColor = 'blue';

        // 清楚 container 中所有
        while (xy_mousemove.firstChild) {
            xy_mousemove.removeChild(xy_mousemove.firstChild);
        }
        xy_mousemove.appendChild(verticalLine);
        xy_mousemove.appendChild(horizontalLine);



    });

    // 点击鼠标时//////////////////////////////
    document.addEventListener('click', function (event) {
        var x = event.clientX;
        var y = event.clientY;
        let targetElement = event.target;


        // 检查目标元素及其父级是否具有.control_ele_area类
        while (targetElement !== null) {
            if (targetElement.classList.contains('control_ele_area')) {
                // 如果目标元素或其父级之一具有.control_ele_area类，则拒绝响应
                return;
            }
            // 继续检查父级元素
            targetElement = targetElement.parentElement;
        }

        // 填写某一个边距信息
        fill_video_size(x, y)

        // 填写水印下边距
        fill_watermark_bottom(x, y)
    })



}