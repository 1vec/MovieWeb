<template>
	<div>
		<head-top></head-top>

		<div>			
			<el-container>

			

			<el-main>

				<!-- <div class="bg" :style='{background-image: "url(" + require("../assest/img/banner,jpg") + ")"}'></div> -->
				<div class="explore">
				<el-row>电影，</el-row>
				<el-row>你知道吗？</el-row>
				</div>

			</el-main>
			


			<el-footer height="100%">
	          	<el-row type="flex" justyfy="space-around">
		            <el-col :span="5" :offset="2">
			            <div class="foot-logo">
			                <div class="logo">
			            	    <a>Movie<span>Nest</span></a>
			                	<p>最好的电影分析工具</p>
			                </div>
			            </div>
		            </el-col>
	            	<el-col :span="5">
	              		<h4>链接</h4>
	              		<p><a>主页</a></p>
	              		<p><a>票房分析</a></p>
	              		<p><a>评分分析</a></p>
	            	</el-col>
	            	<el-col :span="5">
	              		<h4>经典电影</h4>
	              		<p><a href="https://en.wikipedia.org/wiki/L%C3%A9on:_The_Professional">这个杀手不太冷（1994）</a></p>
	              		<p><a href="https://en.wikipedia.org/wiki/Titanic_(1997_film)">泰坦尼克号（1997）</a></p>
	              		<p><a href="https://en.wikipedia.org/wiki/Flipped_(film)">怦然心动（2010）</a></p>
	              		<p><a href="https://en.wikipedia.org/wiki/The_Matrix">黑客帝国（1999）</a></p>
	              		<p><a href="https://en.wikipedia.org/wiki/Roman_Holiday">罗马假日（1953）</a></p>
	            	</el-col>
	            	<el-col :span="5">
	              		<h4>联系方式</h4>
	              		<p>518000</p>
	              		<p>广东省深圳市南山区</p>
	              		<p class="foot-email"><a href="http://www.hitsz.edu.cn/home.html">哈尔滨工业大学（深圳）</a></p>
	            	</el-col>
	          	</el-row>
	        </el-footer>


			</el-container>
		</div>



	</div>
</template>


<script>
	import headTop from '../components/headTop'

	export default{
		data(){
			// return {
			// 	note: {
			// 		background-image: "url(" + require("../assest/img/banner,jpg") + ")" ,
			// 	},
			// }
		},
		components: {
			headTop,
		},
		

	}
</script>


<style lang="less">
	@import '../style/mixin';

	/*主体*/

	.el-main{
	  position: relative;	  
	  //background: url(../assets/img/banner.jpg)no-repeat;
	  min-height: 1000px;
	  color: #fff;
	  .bg{
	  	height: 100%;
	  	width: 100%;
	  	position: absolute;
	  	z-index: -1;
	  	background-size: cover;
	  	background-repeat: no-repeat;
	  	filter: blur(5px);
	  }
	}

	// .el-main:before{
	//   background: rgba(0,122,207,.4);
	//   position: absolute;
	//   width: 100%;
	//   height: 100%;
	//   content: "";
	// }

	.el-main .el-row{
	  font-size: 80px;
	}

	.explore{
	  margin: 220px;
	  // margin-left: 10%;
	}



	/*脚注*/

	.el-footer{
	  padding: 70px;
	}

	.el-footer p{
	  margin: 0;
	  margin-bottom: 8px;
	}

	.el-footer p, a{
	  color: #565a5c;
	  transition:all .5s;
	}

	.el-footer a:hover{
	  transform: scaleX(1.2);
	  color: #00d8ff;
	}

	.foot-logo{
	  padding-top: 40px;
	}

	.logo a, .logo a:hover{
	  color: #565a5c;
	  font-size:24px;
	  text-transform: capitalize;
	}

	.logo a>span{
	  color: #00d8ff;
	}


</style>