# Backend Setup Instructions

## 1. MongoDB Atlas Configuration

The 500 errors you're seeing are because MongoDB is not configured. Follow these steps:

### Step 1: Create a MongoDB Atlas Account
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for a free account
3. Create a new project

### Step 2: Create a Database Cluster
1. Click "Build a Database"
2. Choose the free tier (M0)
3. Select your preferred region
4. Create the cluster and wait for it to initialize (5-10 minutes)

### Step 3: Create Database User
1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Set username: `unipath_admin`
4. Set password: (generate a strong password or use your own)
5. Click "Add User"

### Step 4: Allow IP Access
1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. For development, click "Allow Access from Anywhere" (0.0.0.0/0)
4. **For production, only allow your server's IP address**

### Step 5: Get Connection String
1. Go back to "Clusters" view
2. Click "Connect" on your cluster
3. Select "Connect your application"
4. Copy the MongoDB connection string
5. It should look like:
   ```
   mongodb+srv://unipath_admin:PASSWORD@cluster.mongodb.net/unipath_ghana?retryWrites=true&w=majority
   ```
6. **Replace `PASSWORD` with your actual password**

## 2. Configure Backend Environment

### Step 1: Create `.env` file
1. In the `backend/` directory, copy `.env.example` to `.env`:
   ```bash
   cd backend
   cp .env.example .env
   ```

### Step 2: Edit `.env` file
Open `backend/.env` and update these values:

```env
# Your MongoDB connection string from Step 5 above
MONGO_URI=mongodb+srv://unipath_admin:YOUR_PASSWORD@cluster.mongodb.net/unipath_ghana?retryWrites=true&w=majority

# Keep these for development (change for production)
FLASK_ENV=development
SECRET_KEY=dev-secret-key-2024
JWT_SECRET_KEY=dev-jwt-secret-2024

# Frontend URL (where your React app runs)
FRONTEND_URL=http://localhost:5173

# Optional: Anthropic API for AI explanations
ANTHROPIC_API_KEY=your-api-key-here
```

### Step 3: Seed the Database
Once MongoDB is connected, populate the database with initial data:

```bash
cd backend
python scripts/seed_database.py
```

This will create:
- Sample universities
- Sample courses
- Sample cut-off points
- Sample career paths

## 3. Start the Backend Server

```bash
cd backend
source venv/bin/activate    # Windows: venv\Scripts\activate
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

The 500 errors should now be gone, and the `/api/courses`, `/api/universities`, and `/api/careers` endpoints should work.

## 4. Troubleshooting

### Still getting 500 errors?
1. Check that `.env` has the correct `MONGO_URI`
2. Verify your MongoDB username/password are correct
3. Check that IP whitelist includes your machine
4. Look at the terminal where `python run.py` is running for error messages

### Profile validation still failing?
Make sure you've filled ALL of these in your profile:
- ✅ SHS Program (e.g., "Science", "Business", "General")
- ✅ WASSCE Subjects and Grades
- ✅ **Interests** (at least one from the list: Tech & Computing, Health Sciences, Engineering, Business, Arts, Social Sciences, Entrepreneurship)
- ✅ **Skills** (at least one with a rating: Analytical Thinking, Problem Solving, Mathematics, Communication, Leadership, Creativity, Teamwork)
- ✅ **Career Goals** (at least one: Software Engineer, Doctor, Lawyer, Engineer, Accountant, Data Scientist)

All three sections (Interests, Skills, Career Goals) must be filled before requesting recommendations.
