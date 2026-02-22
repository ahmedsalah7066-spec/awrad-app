package com.example.awrad

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject
import androidx.lifecycle.lifecycleScope
import com.example.awrad.data.repository.SimpleContentRepository
import kotlinx.coroutines.launch
import java.util.Locale

@AndroidEntryPoint
class MunajatListActivity : BaseActivity() {

    @Inject
    lateinit var repository: SimpleContentRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Reusing the same layout as AwradListActivity since it's identical structure
        setContentView(R.layout.activity_awrad_list)

        // Header Setup
        val headerView = findViewById<View>(R.id.header)
        applyHeaderInsets(headerView)

        val titleView = findViewById<TextView>(R.id.tvHeaderTitle)
        val backButton = findViewById<ImageView>(R.id.btnBack)
        
        titleView.text = getString(R.string.munajat_title)
        
        backButton.setOnClickListener {
            finish()
        }

        applyWindowInsets(findViewById(android.R.id.content))

        // RecyclerView Setup
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        
        // Load data properly
        lifecycleScope.launch {
            val lang = LocaleManager.getLanguage(this@MunajatListActivity)
            val items = repository.getAllMunajats(lang)
            recyclerView.adapter = MunajatAdapter(items)
        }
    }

    inner class MunajatAdapter(private val items: List<Munajat>) : RecyclerView.Adapter<MunajatAdapter.ViewHolder>() {

        inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
            val title: TextView = view.findViewById(R.id.tvTitle)
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
            val view = LayoutInflater.from(parent.context)
                .inflate(R.layout.item_simple_list, parent, false)
            return ViewHolder(view)
        }

        override fun onBindViewHolder(holder: ViewHolder, position: Int) {
            val item = items[position]
            val title = if (item.titleResId != 0) getString(item.titleResId) else item.title ?: ""
            holder.title.text = title
            
            holder.itemView.setOnClickListener {
                val intent = Intent(this@MunajatListActivity, MunajatDetailActivity::class.java)
                intent.putExtra("munajat_index", position)
                startActivity(intent)
            }
        }

        override fun getItemCount() = items.size
    }
}
