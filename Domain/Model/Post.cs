using System;

namespace Domain.Model
{
    public class Post
    {
        public string Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public DateTime TimeStamps { get; set; }       
        public PostLocation Location { get; set; } 
    }
}