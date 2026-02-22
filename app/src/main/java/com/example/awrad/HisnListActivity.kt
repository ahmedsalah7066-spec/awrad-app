package com.example.awrad

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.activity.viewModels
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class HisnListActivity : BaseActivity() {

    private val viewModel: HisnViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hisn_list)

        val titleView = findViewById<TextView>(R.id.tvHeaderTitle)
        titleView.text = getString(R.string.hisn_muslim_title)

        val recyclerView = findViewById<RecyclerView>(R.id.rvCategories)
        recyclerView.layoutManager = LinearLayoutManager(this)

        // Initialize adapter with empty list
        val adapter = HisnCategoryAdapter(emptyList()) { category ->
            val intent = Intent(this, HisnDetailActivity::class.java)
            intent.putExtra("categoryId", category.id)
            startActivity(intent)
        }
        recyclerView.adapter = adapter

        // Observe categories
        viewModel.categories.observe(this) { categories ->
            adapter.updateList(categories)
        }
    }
}

class HisnCategoryAdapter(
    private var list: List<HisnCategory>,
    private val onClick: (HisnCategory) -> Unit
) : RecyclerView.Adapter<HisnCategoryAdapter.ViewHolder>() {

    fun updateList(newList: List<HisnCategory>) {
        list = newList
        notifyDataSetChanged()
    }

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title: TextView = view.findViewById(R.id.tvTitle)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_hisn_category_styled, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = list[position]
        val context = holder.itemView.context
        holder.title.text = item.title ?: context.getString(item.titleResId)
        
        holder.itemView.setOnClickListener { onClick(item) }
    }

    override fun getItemCount() = list.size}
