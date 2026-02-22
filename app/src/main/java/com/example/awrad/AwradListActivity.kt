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

import androidx.activity.viewModels
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class AwradListActivity : BaseActivity() {

    private val viewModel: AwradListViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_awrad_list)

        // Header Setup
        val headerView = findViewById<View>(R.id.header)
        applyHeaderInsets(headerView)

        val titleView = findViewById<TextView>(R.id.tvHeaderTitle)
        val backButton = findViewById<ImageView>(R.id.btnBack)
        
        titleView.text = getString(R.string.dalail_title)
        
        backButton.setOnClickListener {
            finish()
        }

        applyWindowInsets(findViewById(android.R.id.content))

        // RecyclerView Setup
        val recyclerView = findViewById<RecyclerView>(R.id.recyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)
        
        val adapter = AwradAdapter(emptyList())
        recyclerView.adapter = adapter
        
        viewModel.uiState.observe(this) { list ->
            adapter.updateList(list)
        }
    }
    
    override fun onResume() {
        super.onResume()
        viewModel.loadData() // Refresh on resume (in case language changed)
    }

    inner class AwradAdapter(private var items: List<Awrad>) : RecyclerView.Adapter<AwradAdapter.ViewHolder>() {

        fun updateList(newItems: List<Awrad>) {
            items = newItems
            notifyDataSetChanged()
        }

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
            val title = if (item.dayResId != 0) getString(item.dayResId) else item.dayTitle ?: ""
            holder.title.text = title
            
            holder.itemView.setOnClickListener {
                val intent = Intent(this@AwradListActivity, AwradDetailActivity::class.java)
                intent.putExtra("day_index", position) // Pass index instead of ResId
                intent.putExtra("day_title", title)
                startActivity(intent)
            }
        }

        override fun getItemCount() = items.size
    }
}
