(function(factory){
    if(typeof define === 'function' && define.amd){
        define(['jquery', 'CityData'], factory);
    }else if(typeof exports === 'object'){
        factory(require('jquery'), require('CityData'));
    }else{
        factory(jQuery, CityData);
    }
})(function($, CityData){
    'use strict';
    var CitySelector = function(element, options){
        this.$el     = $(element);
        this.options = options;
        this.init();
    };

    CitySelector.DEFAULTS = {
        country: '86',                           // Country code
        simple: true,                            // Simplified address
        val: '',                                 // Default val
        placeholder: '请选择省市区',               // Placeholder prompt character
        callback: $.noop                        // Callback function with two parameters: selected item, address index
    };

    CitySelector.TEMPLATES = '<div class="city-title"></div>' +
                             '<div class="city-dropdown"></div>' +
                             '<div class="city-wrap">' +
                                 '<div class="city-tabs"></div>' +
                                 '<div class="city-content"></div>' +
                             '</div>';

    $.extend(CitySelector.prototype, {

        /**
         * Initializes the object
         */
        init: function(){
            var self    = this;
            self.items  = [];
            self.DOM    = self.DOM || self.getDom();
            self.bind().reset();
        },

        /**
         * Bind event
         * @return  {CitySelector}
         */
        bind: function(){
            var self    = this;
            var DOM     = self.DOM;

            // Click outside the range
            $(document).on('click.cityselector', function(e){
                var $el = $(e.target).closest('.city-selector');
                if(!$el.length){
                    $('.city-selector.open').removeClass('open');
                }
            });

            // Selector toggle class
            $(DOM.selector).on('click', '.city-title,.city-dropdown',function(){
                $(this).closest('.city-selector').toggleClass('open');
            });

            // Tbas toggle
            $(DOM.tabs).on('click', 'a', function(){
                var $el   = $(this);
                var index = $el.index();
                $el.addClass('active').siblings('a').removeClass('active');
                $('.city-pane', self.DOM.content).removeClass('active').eq(index).addClass('active');
                return false;
            });

            // City select
            $(DOM.content).on('click', '.city-pane a', function(){
                var $el      = $(this);
                var pane     = $el.closest('.city-pane');
                var index    = pane.index();
                var item     = {id:$el.data('id'),address:$el.text()};
                var val;

                // set status
                pane.find('.active').removeClass('active');
                $el.addClass('active');

                // Reset selected items;
                self.items               = self.items.slice(0, index);
                self.items[index++]      = item;
                val                      = self.setContent(index, item.id).getVal(null);
                self.sync(val.join(' '));
                self.DOM.title.innerHTML = val.join('<span>/</span>');
                if($.isFunction(self.options.callback)){
                    self.options.callback.call(self, item, index);
                }

                return false;
            });

            return self;
        },

        /**
         * Sync val
         * @param   {String}    val
         * @return  {CitySelector}
         */
        sync: function(val){
            var self = this;
            var $el  = self.$el;
            var fn   = $el.is('input')?'val':'html';
            $el[fn](val);
            return self;
        },

        /**
         * Unmounts the bind event
         * @return  {CitySelector}
         */
        unbind: function(){
            var self = this;
            var DOM  = self.DOM;
            $(document).off('click.cityselector');
            $(DOM.selector).add(DOM.tabs).add(DOM.content).off('click');
            return self;
        },

        /**
         * Get selected value
         * @param    {String}       separator
         * @param    {String|null}  [type]        null-get All id | address
         * @return   {String|Array}
         */
        getVal: function(separator, type){
            var self = this;
            var val;
            type     = typeof type === 'undefined' ? 'address' : type;
            if(type === null){
                return self.items;
            }

            val = [];
            $.each(self.items, function(key,row){
                if(row){
                    val.push(row[type]);
                }
            });
            return separator === null ? val : val.join(separator);
        },

        /**
         * Set values
         * @param   {String|Array}  val
         * @param   {String}        [placeholder]
         * @retrun  {CitySelector}
         */
        setVal: function(val, placeholder){
            var self    = this;
            var DOM     = self.DOM;
            var panes   = $('.city-pane', DOM.content);
            var $el;

            if(val == ''){
                self.sync('');
                self.items  = [];
                panes.filter(':gt(0)').html('').removeClass('active');
                panes.eq(0).addClass('active').find('.active').removeClass('active');
                $('a', DOM.tabs).removeClass('active').eq(0).addClass('active');
                DOM.title.innerHTML = placeholder || '<span class="placeholder">'+self.options.placeholder+'</span>'
            }else{
                val = typeof val === 'string' ? val.split(' ') : val;
                for(var i = 0; i < val.length; i++){
                    $el = panes.eq(i);
                    if(!!$el.find('.city-loading').length){
                        $el.data('val', self.simplize(val[i], i));
                    }else{
                        $el.find("a:contains('"+self.simplize(val[i], i)+"')").trigger('click');
                    }
                }
            }

            return self;
        },

        /**
         * Set tabs
         * @param   {Object}    data
         * @return  {CitySelector}
         */
        setTabs: function(data){
            var self    = this;
            var DOM     = self.DOM;
            var tabs    = DOM.tabs;
            var content = DOM.content;
            tabs.innerHTML = '';
            content.innerHTML = '';
            $.each(data, function(k,v){
                tabs.innerHTML    += '<a href="javascript:;">'+v+'</a>';
                content.innerHTML += '<div class="city-pane"></div>';
            });
            return self;
        },

        /**
         * Reset form
         * @return  {CitySelector}
         */
        reset: function(){
            var self    = this;
            var options = self.options;
            var data    = CityData[options.country] || {};
            return self.setTabs(data.tabs).setContent(0).setVal(options.val);
        },

        /**
         * Set content
         * @param   {Number}    index
         * @param   {Number}    id
         * @return  {CitySelector}
         */
        setContent: function(index, id){
            var self  = this;
            var DOM   = self.DOM;
            var pane  = $('.city-pane', DOM.content);
            var $el   = pane.eq(index);
            var data, src;

            if(!!$el.length){

                // Set state
                pane.removeClass('active').filter(':gt('+index+')').html('');
                $el.addClass('active');
                $('a', DOM.tabs).removeClass('active').eq(index).addClass('active');

                // Output data
                data = CityData[self.options.country] || {};
                data = data.content && data.content[index] || {};
                if(typeof  data === 'string'){
                    src = self.getVal(null, 'id');
                    $.ajax({
                        url: data + src.slice(0, index).join('/')+'.json',
                        dataType: 'json',
                        beforeSend: function(XHR){
                            var xhr = $el.data('_xhr');
                            if(xhr){
                                xhr.abort();
                            }
                            $el.data('_xhr', XHR).html('<span class="city-loading"></span>');
                        },
                        complete: function(XHR,TS){
                            var res = XHR.responseJSON || {};
                            var val;
                            if(TS != 'abort'){
                                self.outputData(res, $el, index, id);
                                val = $el.data('val');
                                if(val){
                                    $el.find("a:contains('"+val+"')").trigger('click');
                                    $el.removeData('val');
                                }
                            }
                        }
                    });
                }else{
                    self.outputData((id?data[id]:data), $el, index, id);
                }
            }else{
                // Close the drop-down
                $(DOM.selector).removeClass('open');
            }

            return self;
        },

        /**
         * Output city data
         * @param   {Object}        data
         * @param   {HtmlElement}   element
         * @param   {Number}        index
         * @param   {Number}        id
         * @return  {CitySelector}
         */
        outputData: function(data, element, index, id){
            var self  = this;
            var $el   = $(element);
            var list  = [];
            var isStr = false;

            if(data){
                $.each(data || {}, function(key, row){
                    isStr = typeof row === 'string';
                    if(isStr){
                        list.push('<a href="javascript:;" title="'+row+'" data-id="'+key+'">'+self.simplize(row, index)+'</a>');
                    }else{
                        list.push('<dl class="clearfix"><dt>'+key+'</dt><dd>');
                        $.each(row, function(k, v){
                            list.push('<a href="javascript:;" title="'+v[1]+'" data-id="'+v[0]+'">'+self.simplize(v[1], index)+'</a>');
                        });
                        list.push('</dd></dl>');
                    }
                });

                if(isStr){
                    list.unshift('<dl class="clearfix"><dd>');
                    list.push('</dd></dl>');
                }
            }

            $el.html(list.join(''));
            if(id && !list.length){
                // Automatic next level
                self.setContent(index + 1, id);
            }else if(index && list.length == 3){
                // The only quick click
                $el.find('a:first').trigger('click');
            }

            return self;
        },

        /**
         * Simplize address
         * @param   {String}    address
         * @param   {String}    index
         * @return  {String}
         */
        simplize: function(address, index){
            var simple = this.options.simple;
            address    = address || '';

            if(!simple){
                return address;
            }else if($.isFunction(simple)){
                return simple.call(this, address, type);
            }

            switch(index){
                case 0:
                    return address.replace(/省|市|自治区|[壮回]族|维吾尔|特别行政区/g, '');
                case 1:
                    return address.replace(/自治[州县]|[地林]区|[市盟县]|(?:回|藏|土家|苗|黎|布依|侗|蒙古|羌|彝|哈尼|白|傣|景颇|傈僳|朝鲜|壮)族|蒙古|哈萨克|特别行政区/g, '');
                case 2: // 伊宁、临夏 有问题
                    return address.length > 2 ? address.substring(0, 2) + address.substring(2).replace(/自治[县旗]|新区|[市县旗区]|(?:满|蒙古|回|达斡尔|哈萨克|克|朝鲜|畲|土家|苗|瑶|侗|壮|各|仫佬|毛南|羌|彝|藏|仡佬|布依|水|傣|哈尼|纳西|拉祜|佤|布朗|独龙|普米|白|怒|傈僳|裕固|保安|东乡|撒拉|土)族|群岛|行政委员会|塔吉克|锡伯|哈萨克|蒙古|特别行政区/g, '') : address;
                case 3:
                    return address.replace(/办事处|地区/g, '');
                default:
                    return address;
            }
        },

        /**
         * Get HtmlElement
         * @return  {object}    DOM
         */
        getDom: function(){
            var $el      = this.$el;
            var width    = $el.css('width');
            var height   = $el.css('height');
            var selector = $('<div>').addClass('city-selector').css({width: width,height:height});
            var DOM      = {selector: selector[0]};
            selector.html(CitySelector.TEMPLATES).insertAfter($el).find('[class^="city-"]').each(function(){
                DOM[this.className.split('city-')[1]] = this;
            });
            $el.data('_display', $el.css('display'));
            $el.hide();
            $(DOM.title).css({height: height,lineHeight: height});
            $(DOM.wrap).css({width: width,left: -1,top:height});
            return DOM;
        },

        /**
         * Set the country
         * @param   {String} country
         * @return  {CitySelector}
         */
        setCountry: function(country){
            var self    = this;
            self.country = country;
            return self.reset();
        },

        /**
         * Destroy the object
         */
        destroy: function(){
            var self    = this;
            var $el     = self.$el;
            var display = $el.data('_display');
            self.unbind();
            $el.css('display', display).removeData('lx.citySelector').show();
            $(self.DOM.selector).remove();
        }
    });

    // CITYSELECTOR PLUGIN DEFINITION
    // ========================
    function Plugin(option){
        var param = [].slice.call(arguments,1);
        return this.each(function(){
            var that    = $(this);
            var data    = that.data('lx.citySelector');
            var fn      = that.is('input')?'val':'html';
            var options = $.extend({}, CitySelector.DEFAULTS, that.data(), {val: that[fn]()}, typeof option == 'object' && option);
            if(!data){
                that.data('lx.citySelector', (data = new CitySelector(this, options)));
            }
            if(typeof option == 'string'){
                data[option].apply(data, param);
            }
        });
    }

    var old = $.fn.citySelector;
    $.fn.citySelector             = Plugin;
    $.fn.citySelector.Constructor = CitySelector;

    // CITYSELECTOR NO CONFLICT
    // ==================
    $.fn.citySelector.noConflict = function(){
        $.fn.citySelector = old;
        return this;
    };
});