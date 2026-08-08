# ======= DELETING UNVERIFIED USERS =======

def delete_unverified_users():
    """
    Connects to the database and deletes users who signed up more than
    24 hours ago and are still not verified.
    """
    try:
        mycon = dbConn()
        cursor = mycon.cursor()

        # Calculate the cutoff time (24 hours ago)
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        # Find unverified users who are older than 24 hours
        cursor.execute(
            "SELECT email FROM login_data WHERE is_verified = false AND created_at < %s",
            (cutoff_time,)
        )
        users_to_delete = cursor.fetchall()
        
        if not users_to_delete:
            print("🧹 No unverified users older than 24 hours to delete.")
            cursor.close()
            mycon.close()
            return 0

        # Delete the identified users
        email_list = [user[0] for user in users_to_delete]
        query = "DELETE FROM login_data WHERE email IN (%s)" % ','.join(['%s'] * len(email_list))
        
        cursor.execute(query, email_list)
        mycon.commit()
        
        deleted_count = cursor.rowcount
        print(f"🧹 Deleted {deleted_count} unverified users: {email_list}")

        cursor.close()
        mycon.close()
        
        return deleted_count

    except Exception as e:
        print(f"❌ Error deleting unverified users: {e}")
        import traceback
        traceback.print_exc()
        return -1