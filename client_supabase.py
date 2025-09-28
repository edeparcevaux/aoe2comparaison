from supabase import create_client, Client
import os

# ⚠️ Mets tes vraies clés et URL ici
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://kjpsykqkjdvayehcxjfd.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqcHN5a3FramR2YXllaGN4amZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkwOTM0NTIsImV4cCI6MjA3NDY2OTQ1Mn0.F8rqp9sn5IicqevWEFmHgkQzP-4D0g0yU56NdteWxCA")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)