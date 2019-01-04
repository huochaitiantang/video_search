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
                        $("#result_div").append("<div>search error: " + ans['error'] + " !</div>");
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
		$("#search_div").append("<div>select videos</div>")
		for(var i = 0; i < video_paths.length; i++){
			var node_string = "<div><video src='" + video_paths[i] + "'></div>";
			$("#search_div").append(node_string);
		}
		$("video").attr({width:"200"})
		$("video").mouseover(function(){
			$(this).attr({controls: "controls"});
		});
		$("video").mouseout(function(){
			$(this).removeAttr("controls");
		});
		$("video").click(function(){
            ss = $(this).attr("src").split('/');
            name_id = ss[ss.length - 1];
			$("#search_content").val(name_id);
		});
	}


	function display_result_videos(video_paths, video_scores){
		$("#result_div").append("<div>result videos/match scores</div>")
		for(var i = 0; i < video_paths.length; i++){
			var node_string = "<div><video src='" + video_paths[i] + "'></video><span>" + video_scores[i] + "</span></div>";
			$("#result_div").append(node_string);
		}
		$("video").attr({width:"200"});
		$("video").mouseover(function(){
			$(this).attr({controls: "controls"});
		});
		$("video").mouseout(function(){
			$(this).removeAttr("controls");
		});
	}

});
