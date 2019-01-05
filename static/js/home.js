$(document).ready(function(){

    // Step 1: init search video
    init_search_video();
    function init_search_video(){		
        var p = get_promise('/home/msg_init');
        p.then(
            (res) => {
                ans = JSON.parse(res);
                console.log(ans);
				display_search_videos(ans['video_paths']);
			});
	}

    // Step 2: click change button to change search videos randomly
	$("#change_button").click(function() {
        var p = get_promise('/home/msg_change');
        p.then(
            (res) => {
                ans = JSON.parse(res);
                console.log(ans);
                $("#search_div").empty();
				display_search_videos(ans['video_paths']);
			});
	});

	// Step 3: click search button to search videos in dataset
	$("#search_button").click(function() {
        name_id = $("#search_content").val();
		console.log(name_id);
        if(name_id.length > 0){
            var p = get_promise('/search/' + name_id);
            p.then(
                (res) => {
                    ans = JSON.parse(res);
                    console.log(ans);
                    $("#result_div").empty();
                    if(ans['cnt'] <= 0){
		                $("#result_div").append("<div style='margin:10px;text-align:center;'>Error: " + ans['error'] + "!</div>")
                    }
                    else{
		    		    display_result_videos(ans['video_paths'], ans['video_scores']);
                    }
		    	});
            }
	});


    function get_promise(url){
    	var p = new Promise(function(resolve, reject){
    		var request = new XMLHttpRequest();
    		request.open('GET', url, true);
    		request.addEventListener("load", function(){
    			resolve(this.responseText);
    		});
    		request.send();
    	});
    	return p;
    }

	function display_search_videos(video_paths){
		$("#search_div").append("<div style='margin:10px;text-align:center;'>select videos</div>")
		for(var i = 0; i < video_paths.length; i++){
			var node_string = "<div style='padding:10px;border: 2px solid #888888; border-radius: 5px; margin: 15px;'><video class='search_video' src='" + video_paths[i] + "'></div>";
			$("#search_div").append(node_string);
		}
		$(".search_video").attr({width:"200"})
		$(".search_video").attr({height:"150"});
		$(".search_video").mouseover(function(){
			$(this).attr({controls: "controls"});
            ss = $(this).attr("src").split('/');
            name_id = ss[ss.length - 1];
			$("#video_name").html(name_id);
		});
		$(".search_video").mouseout(function(){
			$(this).removeAttr("controls");
		});
		$(".search_video").click(function(){
            ss = $(this).attr("src").split('/');
            name_id = ss[ss.length - 1];
			$("#search_content").val(name_id);
		});
	}


	function display_result_videos(video_paths, video_scores){
		$("#result_div").append("<div style='margin:10px;text-align:center;'>result videos / rank")
		for(var i = 0; i < video_paths.length; i++){
			var node_string = "<div style='padding:10px;border: 2px solid #888888; border-radius: 5px; margin: 15px;'><video class='result_video' src='" + video_paths[i] + "'></video><span style='vertical-align:top;margin-left:20px;'>" + video_scores[i] + "</span></div>";
			$("#result_div").append(node_string);
		}
		$(".result_video").attr({width:"200"});
		$(".result_video").attr({height:"150"});
		$(".result_video").mouseover(function(){
			$(this).attr({controls: "controls"});
            ss = $(this).attr("src").split('/');
            name_id = ss[ss.length - 1];
			$("#video_name").html(name_id);
		});
		$(".result_video").mouseout(function(){
			$(this).removeAttr("controls");
		});
	}

});
