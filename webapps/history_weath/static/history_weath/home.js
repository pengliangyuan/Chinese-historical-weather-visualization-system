(function () {
  'use strict'

feather.replace()
	
var page1_chart1 = Highcharts.chart('page1_chart1', {
			chart: {
				type: 'line'
			},
			title: {
				text: ''
			},
			subtitle: {
				text: ''
			},
			xAxis: {
				categories: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
			},
			yAxis: {
				title: {
					text: '气温 (°C)'
				}
			},
			plotOptions: {
				line: {
					dataLabels: {
						// 开启数据标签
						enabled: true          
					},
					// 关闭鼠标跟踪，对应的提示框、点击事件会失效
					enableMouseTracking: false
				}
			},
			series: []
});

var page1_chart2 = Highcharts.chart('page1_chart2', {
			chart: {
				type: 'line'
			},
			title: {
				text: ''
			},
			subtitle: {
				text: ''
			},
			xAxis: {
				categories: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
			},
			yAxis: {
				title: {
					text: '气温 (°C)'
				}
			},
			plotOptions: {
				line: {
					dataLabels: {
						// 开启数据标签
						enabled: true          
					},
					// 关闭鼠标跟踪，对应的提示框、点击事件会失效
					enableMouseTracking: false
				}
			},
			series: []
});


var page1_chart3 = Highcharts.chart('page1_chart3', {
	chart: {
		plotBackgroundColor: null,
		plotBorderWidth: null,
		plotShadow: false,
		type: 'pie'
	},
	title: {
		text: ''
	},
	tooltip: {
		pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	},
	plotOptions: {
		pie: {
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
				enabled: true,
				format: '<b>{point.name}</b>: {point.percentage:.1f} %',
				style: {
					color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
				}
			}
		}
	},
	series: []
});

var page1_chart4 = Highcharts.chart('page1_chart4', {
	chart: {
		plotBackgroundColor: null,
		plotBorderWidth: null,
		plotShadow: false,
		type: 'pie'
	},
	title: {
		text: ''
	},
	tooltip: {
		pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	},
	plotOptions: {
		pie: {
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
				enabled: true,
				format: '<b>{point.name}</b>: {point.percentage:.1f} %',
				style: {
					color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
				}
			}
		}
	},
	series: []
});

$("#page1_index").click(function(){

		$("#page1").show()
		$("#page2").hide()
		$("#page2_index").removeClass("active")
		$("#page1_index").addClass("active")
});

$("#page2_index").click(function(){

		$("#page2").show()
		$("#page1").hide()
		$("#page1_index").removeClass("active")
		$("#page2_index").addClass("active")
});


$(".page1_add_city").click(function(){
		if($(".page1_city_list").text().indexOf($(this).text()) == -1){
			var insert = $(".page1_city_list").first().clone().text($(this).text())
			insert.bind("click", function(){
				$(this).remove()
			})
			$("#page1_city_label").before(insert)
		}
});



$(".page1_add_year").click(function(){
		if($(".page1_year_list").text().indexOf($(this).text()) == -1){
			var insert = $(".page1_year_list").first().clone().text($(this).text())
			insert.bind("click", function(){
				$(this).remove()
			})
			$("#page1_year_label").before(insert)
		}
});


$(".page1_add_year_weath").first().click(function(){
		$("#page1_chart3").hide()
		$("#page1_year_weath").text("气候")
});


$(".page1_add_month_weath").first().click(function(){
		$("#page1_chart4").hide()
		$("#page1_month_weath").text("气候")
});


/* start: 输入下拉功能添加 */
/* 失去焦点导致无法选中 -- remove
$("#page1_input_city").on('focus',function(){
	$("#page1_input_dropdown_menu").addClass("show")
});

$("#page1_input_city").on('blur',function(){
	$("#page1_input_dropdown_menu").removeClass("show")
});
*/

$("#page1_input_city").on('input',function(){
	var city = $(this).val()
	var dropdown_menu = $("#page1_input_dropdown_menu")
	
	if(city != ""){
		dropdown_menu.addClass("show")
		$.ajax({
			type:"POST",
			url:"/history_weath/like_city",
			data:JSON.stringify({city:city}),
			success:function(result){
			
				//删除
				dropdown_menu.empty()

				//添加
				var citys = JSON.parse(result)
				if(citys.length != 0)
				{
					for(var i = 0;i < citys.length; i++){
						var dropdown_item = $('<button class="dropdown-item page1_add_year"></button>');
						dropdown_item.bind("click", function(){
							if($(".page1_city_list").text().indexOf($(this).text()) == -1){
								var insert = $(".page1_city_list").first().clone().text($(this).text())
								insert.bind("click", function(){
									$(this).remove()
								})
								$("#page1_city_label").before(insert)
								
								//删除
								dropdown_menu.empty()

								//失去焦点导致无法选中  -- add
								dropdown_menu.removeClass("show")
							}

						});
						dropdown_item.text(citys[i])
						dropdown_menu.append(dropdown_item)
					}
				}
				else
				{
					var dropdown_item = $('<button class="dropdown-item page1_add_year"></button>');
					dropdown_item.text("没有匹配城市")
					dropdown_menu.append(dropdown_item)
				
				}
			}
		});
	}
	else{
		//删除
		dropdown_menu.empty()

		//失去焦点导致无法选中  -- add
		dropdown_menu.removeClass("show")
	}
	
});
/* end: 输入下拉功能添加 */


$("#page1_send").click(function(){

	var city_list = $(".page1_city_list")
	var citys = []
	for(var i = 1,p = city_list.first().next(); i < city_list.length; i++, p=p.next())
		citys[i-1] = p.text()
	var year_list = $(".page1_year_list")
	var years = []
	for(var i = 1,p = year_list.first().next(); i < year_list.length; i++, p=p.next())
		years[i-1] = p.text()
	if(citys.length > 0 && years.length > 0)
	{
		/* start: 添加年份选择高亮功能 - 高亮*/
		$(this).addClass("active")	
		/* end: 添加年份选择高亮功能*/
		
		/* start: 输入错误提示提示 - 隐藏*/
		$("#page1_input_danger").text("").hide()
		
		/* end: 输入错误提示 - 隐藏*/

		//删除年份天气下拉选项
		for(var z = $(".page1_add_year_weath").first().next(); z.text() != ""; z = $(".page1_add_year_weath").first().next())
		{
			z.remove()
		}

		/* start: 修改城市和年份，隐藏饼图 */
		$("#page1_chart3").hide()
		$("#page1_year_weath").text("气候")
		$("#page1_chart4").hide()
		$("#page1_month_weath").text("气候")
		/* end: 修改城市和年份，隐藏饼图 */
		
		/* start: 曲线图 */
		$("#page1_month_content").hide()
		$(".page1_month.active").removeClass("active")
		/* end: 曲线图 */

		for(var i = 0; i < citys.length; i++)
		{
			for(var j = 0; j < years.length; j++)
			{

		
				//js闭包特性，解决值传递的问题
				(function _(){
					var city = citys[i];
					var year = years[j];
					var text = city + year + "年各种天气所占比例"
					var insert = $(".page1_add_year_weath").first().clone().text(text)
					insert.bind("click", function(){
						$("#page1_chart3").show()
						$("#page1_year_weath").text($(this).text())
						$.ajax({
							type:"POST",
							url:"/history_weath/weath_year_ratio",
							data:JSON.stringify({city:city, year:year}),
							success:function(result){

								//删除数据
								var len = page1_chart3.series.length;
								for(var i = len - 1; i >= 0; i--){
									page1_chart3.series[i].remove();
								}
						

								//新增数据
								var data = JSON.parse(result)
								page1_chart3.addSeries(data);
								

								var title = city + "-" + year +"年各种天气所占比例饼图";
								page1_chart3.setTitle({text:title,useHTML:true})
							}
						});
					})
					$("#page1_year_weath_label").before(insert)
				})();
		
			}
		}

		$.ajax({
			type:"POST",
			url:"/history_weath/temperature_year",
			data:JSON.stringify({citys:citys, years:years}),
			success:function(result){

				//删除数据
				var len = page1_chart1.series.length;
				for(var i = len - 1; i >= 0; i--){
					page1_chart1.series[i].remove();
				}

				//新增数据
				var data = JSON.parse(result)
				for(var i = 0; i < data.length; i++){
					page1_chart1.addSeries(data[i]);
				}

				var title = citys.toString() + "-" + years.toString() +"年月平均气温曲线图";
				page1_chart1.setTitle({text:title,useHTML:true})
				$("#page1_year_content").show()	
			}
		});
	}
	else{
		/* start: 添加年份选择高亮功能 - 消除*/
		$(this).removeClass("active")	
		/* end: 添加年份选择高亮功能*/

		/* start: 输入错误提示提示 - 显示*/
		$("#page1_input_danger").text("请输入城市和年份（城市和年份可以多次输入，比如北京，上海，2011，2012。点击选中的城市和年份可以取消选中）").show()
		
		/* end: 输入错误提示 - 显示*/
		
		//删除年份天气下拉选项
		for(var z = $(".page1_add_year_weath").first().next(); z.text() != ""; z = $(".page1_add_year_weath").first().next())
		{
			z.remove()
		}

		/* start: 修改城市和年份，隐藏饼图 */
		$("#page1_chart3").hide()
		$("#page1_year_weath").text("气候")
		$("#page1_chart4").hide()
		$("#page1_month_weath").text("气候")
		/* end: 修改城市和年份，隐藏饼图 */

		/* start: 曲线图 */
		$("#page1_year_content").hide()
		$("#page1_month_content").hide()
		$(".page1_month.active").removeClass("active")
		/* end: 曲线图 */

	}
});


$(".page1_month").click(function(){
	var city_list = $(".page1_city_list")
	var citys = []
	for(var i = 1,p = city_list.first().next(); i < city_list.length; i++, p=p.next())
		citys[i-1] = p.text()
	var year_list = $(".page1_year_list")
	var years = []
	for(var i = 1,p = year_list.first().next(); i < year_list.length; i++, p=p.next())
		years[i-1] = p.text()
	var month = $(this).attr('month')
	var month_name = $(this).text()
	if(citys.length > 0 && years.length > 0)
	{

		/* start: 添加月份选择高亮功能*/
		$(".page1_month.active").removeClass("active")
		$(this).addClass("active")	
		/* end: 添加月份选择高亮功能*/

		//删除月份天气下拉选项
		for(var z = $(".page1_add_month_weath").first().next(); z.text() != "";z = $(".page1_add_month_weath").first().next())
		{
			z.remove()
		}
		
		/* start: 修改月份，隐藏饼图 */
		$("#page1_chart4").hide()
		$("#page1_month_weath").text("气候")
		/* end: 修改月份，隐藏饼图 */
		
		for(var i = 0; i < citys.length; i++)
		{
			for(var j = 0; j < years.length; j++)
			{
				//js闭包特性，解决值传递的问题
				(function _(){
					var city = citys[i];
					var year = years[j];
					var text = city + year + "年" + month + "月各种天气所占比例"

					var insert = $(".page1_add_month_weath").first().clone().text(text)
						insert.bind("click", function(){
							$("#page1_chart4").show()
							$("#page1_month_weath").text($(this).text())
							$.ajax({
								type:"POST",
								url:"/history_weath/weath_month_ratio",
								data:JSON.stringify({city:city, year:year, month:month}),
								success:function(result){

									//删除数据
									var len = page1_chart4.series.length;
									for(var i = len - 1; i >= 0; i--){
										page1_chart4.series[i].remove();
									}
							

									//新增数据
									var data = JSON.parse(result)
									page1_chart4.addSeries(data);
									

									var title = city + "-" + year +"年" + month + "月" + "各种天气所占比例饼图";
									page1_chart4.setTitle({text:title,useHTML:true})
								}
							});
					})
					$("#page1_month_weath_label").before(insert)
				})();
	
			}
		}


		$.ajax({
			type:"POST",
			url:"/history_weath/temperature_month",
			data: JSON.stringify({citys:citys, years:years, month:month}),
			dataType:'json',
			success:function(result){
					//删除数据
					var len = page1_chart2.series.length;
					for(var i = len - 1; i >= 0; i--){
						page1_chart2.series[i].remove();
					}

					//新增数据
					var data = result
					for(var i = 0; i < data.length; i++){
						page1_chart2.addSeries(data[i]);
					}

					var title = citys.toString() + "-" + years.toString() +"年" + month  + "月日平均气温曲线图";
					page1_chart2.setTitle({text:title,useHTML:true})
					$("#page1_month_content").show()	

			}
		});
	}

});




}())
