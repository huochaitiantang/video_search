$(document).ready(function(){
  
	function get_all_search_videos(){
		var video_paths = new Array()
		for(var i = 1; i < 5; i++){
			video_paths.push("videos/movie_" + i.toString() + ".mp4")
		}
		return video_paths		
	}
  
	function display_search_videos(video_paths){
		$("#search_div").append("<div>select videos</div>")
		for(var i = 0; i < video_paths.length; i++){
			var node_string = "<div><video src='" + video_paths[i] + "'></video></div>"
			$("#search_div").append(node_string)
		}
		$("video").attr({width:"200"})
		$("video").mouseover(function(){
			$(this).attr({controls: "controls"});
			$("#search_content").val($(this).attr("src"))
		});
		$("video").mouseout(function(){
			$(this).removeAttr("controls");
		});
	}
	
	function display_result_videos(video_paths){
		$("#result_div").append("<div>result videos</div>")
		for(var i = 0; i < video_paths.length; i++){
			var node_string = "<div><video src='" + video_paths[i] + "'></video></div>"
			$("#result_div").append(node_string)
		}
		$("video").attr({width:"200"})
		$("video").mouseover(function(){
			$(this).attr({controls: "controls"});
			//$("#search_content").val($(this).attr("src"))
		});
		$("video").mouseout(function(){
			$(this).removeAttr("controls");
		});
	}
	
	search_video_paths = get_all_search_videos()
	display_search_videos(search_video_paths)

	$("#search_button").click(function() {
		console.log($("#search_content").val())
		display_result_videos(search_video_paths)
	});
	
});