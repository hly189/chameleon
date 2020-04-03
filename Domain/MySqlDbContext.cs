using System;
using Domain.Model;
using Microsoft.EntityFrameworkCore;

namespace Domain
{
    public class MySqlDbContext : DbContext
    {
        public DbSet<Post> Posts { get; set; }
    }
}
