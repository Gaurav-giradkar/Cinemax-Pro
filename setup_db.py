import mysql.connector
import datetime

config_no_db = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root123'
}

def setup():
    conn = mysql.connector.connect(**config_no_db)
    cursor = conn.cursor()
    
    with open('schema.sql', 'r') as f:
        sql = f.read()
    
    # execute schema
    for result in cursor.execute(sql, multi=True):
        pass
    
    conn.database = 'cinemax_pro'
    
    # Add movies
    movies = [
        ('Dune: Part Two', 'Sci-Fi/Adventure', 'PG-13', 'https://images.unsplash.com/photo-1542204165-65bf26472b9b?auto=format&fit=crop&q=80&w=600'),
        ('Oppenheimer', 'Biography/Drama', 'R', 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&q=80&w=600'),
        ('The Batman', 'Action/Crime', 'PG-13', 'https://images.unsplash.com/photo-1509347528160-9a9e33742cb3?auto=format&fit=crop&q=80&w=600'),
        ('Inception', 'Sci-Fi/Action', 'PG-13', 'https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?auto=format&fit=crop&q=80&w=600'),
        ('Interstellar', 'Sci-Fi/Drama', 'PG-13', 'https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=600')
    ]
    cursor.executemany("INSERT INTO movies (title, genre, rating, poster) VALUES (%s, %s, %s, %s)", movies)
    
    # Add theatres
    theatres = [('PVR Cinemas',), ('INOX',), ('Cinepolis',)]
    cursor.executemany("INSERT INTO theatres (name) VALUES (%s)", theatres)
    
    # Add shows (Today and Tomorrow)
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    dates = [today, tomorrow]
    times = ['10:00 AM', '2:00 PM', '6:00 PM', '9:00 PM']
    
    shows = []
    # Mix of movies and theatres
    for d in dates:
        for t_id in range(1, 4):
            for m_id in range(1, 6):
                shows.append((m_id, t_id, d, times[m_id % 4]))
                
    cursor.executemany("INSERT INTO shows (movie_id, theatre_id, date, time) VALUES (%s, %s, %s, %s)", shows)
    
    # Add seats
    cursor.execute("SELECT id FROM shows")
    show_ids = [row[0] for row in cursor.fetchall()]
    
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    seats_data = []
    for s_id in show_ids:
        for r in rows:
            for c in range(1, 11):
                seat_number = f"{r}{c}"
                price = 250.00 if r in ['I', 'J'] else (200.00 if r in ['E', 'F', 'G', 'H'] else 150.00)
                seats_data.append((s_id, seat_number, price))
                
    # batch insert seats
    batch_size = 5000
    for i in range(0, len(seats_data), batch_size):
        cursor.executemany("INSERT INTO seats (show_id, seat_number, price) VALUES (%s, %s, %s)", seats_data[i:i+batch_size])
        
    conn.commit()
    print("Database setup complete.")
    conn.close()

if __name__ == '__main__':
    setup()
