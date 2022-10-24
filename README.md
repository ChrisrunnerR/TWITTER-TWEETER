Socket Programming 
	•	Christopher Stone (castone7)

	•	Message format:
	•	Register: register @handle_A IP_A P1 P2 P3
(Notes: Must not add extra space after the command, it’s counting for the number of words in the command. 1 handle, 1 IP, and 3 ports, don’t add “ “ after the ports)
	•	This command is used for registering a user to the tweeter application. It will take a handle (username), an IP address, and 3 ports (one for communication between the tracker and itself, and the two others for following)
Example: register @bryan 192.168.1.1 13000 13001 13002
	•	Query handles: query handles
	•	This command will return to the client a list of handles that are currently registered in the tweeter application.
	•	Follow: follow @handle_A @handle_B
	•	This command is used for controlling the “following” functionality. The order is: @handle_A follows @handle_B.
Example: follow @bryan @chris
	•	Unfollow: drop @handle_A @handle_B
	•	This command is used for controlling the “unfollowing” functionality. The order is: @handle_A unfollows @handle_B.
Example: drop @bryan @chris
	•	Tweet: tweet @handle message
	•	This command is used for sending a tweet (message).
Example: tweet @handle_A hello world

	•	End Tweet: end tweet
	•	This command is used for making sure all the tweets are sent in the correct order.
Example: end tweet

	•	Exit: exit
	•	This command is used for exiting the program.
Example: exit


	•	Time-Space Diagram









	•	Data Structures & Algorithms Used
	- Queue is used to hold the messages, so it’s processed in the right (First-In-First-Out) order.
	- List (array) is used to maintain the user table as it’s easy to sort a list and print it directly to the screen. We were considering the use of Hash-Map (dictionary), but we figured we didn’t need to access by keys in this case. Sorting is easy in list, but its time complexity is O(n log n).
	- Dictionary (hash-map) — {Key: @handle, Value: List of followers} is used to maintain the follower table, as we can easily search for specific user to get the list of followers of that user. Searching in dictionary is O(1), that’s why we used it. We were trying to use list at first because it was simpler to sort the data in alphabetical order like we did with on the user table.

	•	Github Commits
Link:
https://github.com/ChrisrunnerR/TWITTER-TWEETER




	•	Video Demonstration
Link:
https://www.youtube.com/watch?v=LWryZv0QWpY&ab_channel=ChristopherRunningVlogs
(Timestamp is in the description of the video)
Starting Server - 0:00
Register - 2:05
Follow - 3:57
Query Handles - 5:45
Tweet - 6:00
End-Tweet 6:47
Drop - 7:50
Exit - 9:18
