namespace Domain.Model
{
    public class PostLocation
    {
        public string Id { get; set; }
        public string City { get; set; }
        public string State { get; set; }
        public string ZipCode { get; set; }
        // Google Maps integration
        public long Longtitude { get; set; }
        public long Latitude { get; set; }
    }
}