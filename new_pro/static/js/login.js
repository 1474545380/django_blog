var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        mobile:'',
        password:'',
        remembered:'',
    },
    mounted(){
       
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
        //检查手机号
        check_mobile:function () {
            
        },
        //检查密码
        check_mobile:function () {
            
        },
        //提交
        on_submit:function () {
            
        }
    }
});
function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split('；');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return decodeURIComponent(escape(c.substring(nameEQ.length,c.length).replace(/"/g, "")));
    }
    return null;
}