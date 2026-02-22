package com.example.awrad

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.animation.AnimationUtils
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity

class SplashActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)

        val logo = findViewById<ImageView>(R.id.ivSplashLogo)
        
        // Simple scale animation
        logo.alpha = 0f
        logo.scaleX = 0.5f
        logo.scaleY = 0.5f
        
        logo.animate()
            .alpha(1f)
            .scaleX(1f)
            .scaleY(1f)
            .setDuration(1000)
            .withEndAction {
                // Wait a little bit more then start MainActivity
                Handler(Looper.getMainLooper()).postDelayed({
                    startActivity(Intent(this, MainActivity::class.java))
                    finish()
                }, 500)
            }
            .start()
    }
}
