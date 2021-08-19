var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        is_login:true,
        username:''
    },
    mounted(){
        this.username=getCookie('username');
        this.is_login=getCookie('is_login');
        // this.is_login=true
    },
    methods: {
        //显示下拉菜单
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
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