package com.example.awrad

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.widget.ImageView
import com.google.android.material.card.MaterialCardView
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class AboutActivity : BaseActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about)

        applyWindowInsets(findViewById(android.R.id.content))

        findViewById<ImageView>(R.id.btnBack).setOnClickListener {
            finish()
        }
        
        findViewById<MaterialCardView>(R.id.cardContactUs).setOnClickListener {
            val email = getString(R.string.contact_email)
            val intent = Intent(Intent.ACTION_SENDTO).apply {
                data = Uri.parse("mailto:$email")
                putExtra(Intent.EXTRA_SUBJECT, "تطبيق أوراد - ملاحظات ومقترحات")
            }
            try {
                startActivity(Intent.createChooser(intent, "اختر تطبيق البريد الإلكتروني"))
            } catch (e: Exception) {
                android.widget.Toast.makeText(this, "لا يوجد تطبيق بريد إلكتروني مثبت", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
    }
}
