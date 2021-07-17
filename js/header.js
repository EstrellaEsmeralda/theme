$(document).ready(function() {
    $('a.static-search-toggle-btn').on('click', function(e) {
        e.preventDefault();
        $(this).next().toggleClass('o_hidden');
    });

    $('a#user_account').on('click', function(e) {
        $('div.toggle-config').toggleClass("o_hidden");
    });
});

odoo.define('theme_scita.cstm_toggle_menu', function(require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.toggle_nav_menu = publicWidget.Widget.extend({
        selector: ".nav-items-icon",
        start: function () {
            self = this;
            self.showToggleMenu();
        },
        showToggleMenu: function(){
            $('.nav-toggle-btn').on('click',function(e){
                $('#cstm-nav-menu-toggle').removeClass("o_hidden");
                $('body').addClass('show-scita-cstm-menu');
            });
            $('#close_cstm_nav_toggle').on('click', function(e) {
                $('#cstm-nav-menu-toggle').addClass("o_hidden");
                $('body').removeClass('show-scita-cstm-menu');
            }); 
        },
    });
});

odoo.define('theme_scita.search_menu_js', function(require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.show_search_bar = publicWidget.Widget.extend({
        selector: ".hm-search",
        start: function () {
            self = this;
            self.showSearchBar();
        },
        showSearchBar: function(){
            $('a.static-search').on('click', function(e) {
                e.preventDefault();
                $('.header-search').removeClass("o_hidden");
                var $header_affix = $('header.sct_header_disp.o_header_affix')
                if ($header_affix) {
                    $header_affix.find('div.header-search').replaceWith();
                }
            });
        },
    });
});

odoo.define('theme_scita.search_toggle_js', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.search_toggle_box = publicWidget.Widget.extend({
        selector: ".o_header_affix .hm-search-toggle",
        start: function () {
            self = this;
            self.toggleSearchBox();
        },
        toggleSearchBox: function(){
            $('header.o_header_affix').find('a.static-search-toggle-btn').bind('click', function(e) {
                e.preventDefault();
                if($(this).next().hasClass('o_hidden')){
                    $(this).next().removeClass('o_hidden');
                }else{
                    $(this).next().addClass('o_hidden');
                }
            });
        },
    });
});
    

$(document).click(function(e) {
    if (e.target.id !== 'user_account_icon') {
        if (!$('div.toggle-config').hasClass('o_hidden')) {
            $('div.toggle-config').addClass('o_hidden');
        }
    }
           
    $('span#close_search_bar').on('click', function(e) {
        $('.header-search').addClass("o_hidden");
    });
});
