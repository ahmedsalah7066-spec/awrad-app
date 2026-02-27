package com.example.awrad

import android.content.Context
import android.content.SharedPreferences
import android.os.Build
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.viewModels
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch
import dagger.hilt.android.AndroidEntryPoint
import com.example.awrad.LocaleManager // Explicit Import just in case

@AndroidEntryPoint
class HisnDetailActivity : BaseActivity() {

    private val viewModel: HisnViewModel by viewModels()
    private lateinit var sharedPreferences: SharedPreferences
    private lateinit var adapter: DhikrPagerAdapter
    private lateinit var viewPager: ViewPager2
    private lateinit var tvLargeCounter: TextView
    private lateinit var tvTargetCount: TextView
    private lateinit var tvPageIndicator: TextView
    private var categoryId: String = ""
    private var currentFontSize: Float = 18f

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_hisn_detail)
        applyWindowInsets(findViewById(android.R.id.content))

        sharedPreferences = getSharedPreferences("hisn_prefs", Context.MODE_PRIVATE)
        categoryId = intent.getStringExtra("categoryId") ?: ""

        // Set initial font size based on category
        val fontPrefs = getSharedPreferences("font_prefs", Context.MODE_PRIVATE)
        val defaultSize = if (categoryId == "tasbeehat") 35f else 18f
        currentFontSize = fontPrefs.getFloat("hisn_font_size_$categoryId", defaultSize)

        // Header Setup
        val headerView = findViewById<View>(R.id.header)
        applyHeaderInsets(headerView)
        
        val titleView = findViewById<TextView>(R.id.tvHeaderTitle)
        val backButton = findViewById<ImageView>(R.id.btnBack)
        val shareButton = findViewById<ImageView>(R.id.btnHeaderShare)
        
        backButton.setOnClickListener { finish() }

        shareButton.visibility = View.VISIBLE
        shareButton.setOnClickListener { shareCurrentPage() }

        viewPager = findViewById(R.id.viewPager)
        tvLargeCounter = findViewById(R.id.tvLargeCounter)
        tvTargetCount = findViewById(R.id.tvTargetCount)
        tvPageIndicator = findViewById(R.id.tvPageIndicator)

        findViewById<View>(android.R.id.content).setOnClickListener { incrementCounter() }
        viewPager.setOnClickListener { incrementCounter() }

        initControls()

        // Set Category Title
        viewModel.categories.observe(this) { categories ->
            val category = categories.find { it.id == categoryId }
            if (category != null) {
                titleView.text = if (!category.title.isNullOrEmpty()) {
                    category.title
                } else if (category.titleResId != 0) {
                    getString(category.titleResId)
                } else {
                    categoryId
                }
            }
        }

        // Load Items
        // Load Items
        lifecycleScope.launch {
            val items = viewModel.getHisnItems(categoryId)
            if (items.isNotEmpty()) {
                setupViewPager(items)
            }
        }
        
        viewModel.refresh()
    }

    private fun initControls() {
        val counterArea = findViewById<View>(R.id.bottomCounterArea)
        counterArea?.setOnClickListener { incrementCounter() }
        tvLargeCounter.setOnClickListener { incrementCounter() }

        findViewById<View>(R.id.btnIncreaseFont).setOnClickListener {
            currentFontSize += 2f
            if (::adapter.isInitialized) adapter.setFontSize(currentFontSize)
            getSharedPreferences("font_prefs", Context.MODE_PRIVATE).edit().putFloat("hisn_font_size_$categoryId", currentFontSize).apply()
        }
        findViewById<View>(R.id.btnDecreaseFont).setOnClickListener {
            if (currentFontSize > 12f) {
                currentFontSize -= 2f
                if (::adapter.isInitialized) adapter.setFontSize(currentFontSize)
                getSharedPreferences("font_prefs", Context.MODE_PRIVATE).edit().putFloat("hisn_font_size_$categoryId", currentFontSize).apply()
            }
        }

        val btnReset = findViewById<View>(R.id.btnReset)
        btnReset.setOnClickListener {
            if (::adapter.isInitialized) {
                for (i in 0 until adapter.itemCount) {
                    adapter.setCount(i, 0)
                    saveCount(i, 0)
                }
                adapter.notifyDataSetChanged()
                updateUI(viewPager.currentItem)
                android.widget.Toast.makeText(this, "تم إعادة ضبط العدادات", android.widget.Toast.LENGTH_SHORT).show()
            }
        }
        
        findViewById<View>(R.id.btnNext).setOnClickListener {
            if (::adapter.isInitialized && viewPager.currentItem < adapter.itemCount - 1) {
                viewPager.currentItem += 1
            }
        }
        findViewById<View>(R.id.btnPrev).setOnClickListener {
            if (::viewPager.isInitialized && viewPager.currentItem > 0) {
                viewPager.currentItem -= 1
            }
        }
    }

    private fun setupViewPager(items: List<DhikrItem>) {
        val savedCounts = IntArray(items.size)
        for (i in items.indices) {
            savedCounts[i] = sharedPreferences.getInt("count_${categoryId}_$i", 0)
        }

        val currentLang = LocaleManager.getLanguage(this)
        adapter = DhikrPagerAdapter(items, savedCounts, categoryId, currentLang) {
            incrementCounter()
        }
        adapter.setFontSize(currentFontSize)
        viewPager.adapter = adapter

        viewPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                super.onPageSelected(position)
                updateUI(position)
            }
        })
        
        val lastPage = sharedPreferences.getInt("last_page_${categoryId}", 0)
        val targetPage = if (lastPage < items.size) lastPage else 0
        
        if (targetPage > 0) {
            // Need to post to make sure it's applied correctly
            viewPager.post {
                viewPager.setCurrentItem(targetPage, false)
            }
        }
        
        updateUI(targetPage)
    }

    override fun onPause() {
        super.onPause()
        if (::viewPager.isInitialized) {
            sharedPreferences.edit().putInt("last_page_${categoryId}", viewPager.currentItem).apply()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        if (isFinishing) {
            clearCategoryProgress()
        }
    }

    private fun clearCategoryProgress() {
        val editor = sharedPreferences.edit()
        editor.remove("last_page_${categoryId}")
        
        val allEntries = sharedPreferences.all
        for (key in allEntries.keys) {
            if (key.startsWith("count_${categoryId}_")) {
                editor.remove(key)
            }
        }
        editor.apply()
    }


    private fun updateUI(position: Int) {
        if (!::adapter.isInitialized) return
        val count = adapter.getCount(position)
        val target = adapter.getTargetCount(position)
        
        tvLargeCounter.text = "$count / $target"
        tvPageIndicator.text = "${position + 1} / ${adapter.itemCount}"
        
        val btnReset = findViewById<View>(R.id.btnReset)
        if (position == 0) {
            btnReset.visibility = View.VISIBLE
        } else {
            btnReset.visibility = View.INVISIBLE
        }
    }

    private fun incrementCounter() {
        try {
            if (!::viewPager.isInitialized || !::adapter.isInitialized || !::tvLargeCounter.isInitialized) return

            val position = viewPager.currentItem
            if (position < 0 || position >= adapter.itemCount) return

            val currentCount = adapter.getCount(position)
            val targetCount = adapter.getTargetCount(position)

            if (targetCount == 0 || currentCount < targetCount) {
                val newCount = currentCount + 1
                adapter.setCount(position, newCount)
                tvLargeCounter.text = "$newCount / $targetCount"
                saveCount(position, newCount)

                if (targetCount > 0 && newCount == targetCount) {
                    vibrate(100)
                    if (position < adapter.itemCount - 1) {
                        viewPager.currentItem = position + 1
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    private fun saveCount(index: Int, count: Int) {
        sharedPreferences.edit().putInt("count_${categoryId}_$index", count).apply()
    }

    private fun shareCurrentPage() {
        if (!::adapter.isInitialized || !::viewPager.isInitialized) return
        val position = viewPager.currentItem
        val item = adapter.getItem(position) ?: return
        
        val shareText = buildString {
            append(item.content)
            append("\n\n")
            val fadlText = item.fadl
            if (fadlText.isNotEmpty()) {
                 append("--- الفضل ---\n")
                 append(fadlText).append("\n\n")
            }
            append("تم النسخ من تطبيق أوراد")
        }

        val shareIntent = android.content.Intent(android.content.Intent.ACTION_SEND)
        shareIntent.type = "text/plain"
        shareIntent.putExtra(android.content.Intent.EXTRA_SUBJECT, findViewById<TextView>(R.id.tvHeaderTitle).text)
        shareIntent.putExtra(android.content.Intent.EXTRA_TEXT, shareText)
        startActivity(android.content.Intent.createChooser(shareIntent, "Share Azkar via"))
    }

    private fun vibrate(duration: Long = 50) {
        val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val vibratorManager = getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as android.os.VibratorManager
            vibratorManager.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator.vibrate(VibrationEffect.createOneShot(duration, 255))
        } else {
            @Suppress("DEPRECATION")
            vibrator.vibrate(duration)
        }
    }
}

class DhikrPagerAdapter(
    private val list: List<DhikrItem>,
    private val counts: IntArray,
    private val categoryId: String,
    private val languageCode: String = "en",
    private val onItemClick: () -> Unit
) : RecyclerView.Adapter<DhikrPagerAdapter.ViewHolder>() {

    private var fontSize: Float = if (categoryId == "tasbeehat") 35f else 18f

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val itemRoot: View = view.findViewById(R.id.itemRoot)
        val content: TextView = view.findViewById(R.id.tvArabic) // Renamed property, kepy ID
        val translation: TextView = view.findViewById(R.id.tvTranslation)
        val fadl: TextView = view.findViewById(R.id.tvFadl)
        val imgSeparator1: ImageView = view.findViewById(R.id.imgSeparator1)
        val imgSeparator2: ImageView = view.findViewById(R.id.imgSeparator2)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_dhikr_page, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val item = list[position]
        
        holder.content.text = item.content
        holder.content.textSize = fontSize
        
        // Show Translation based on language code
        // STRICT: Only show requested language, do NOT fallback to English
        // New Logic: translation field in DhikrItem is already localized or empty
        val translationText = item.translation
        if (translationText.isNotEmpty()) {
            holder.translation.text = translationText
            holder.translation.visibility = View.VISIBLE
            holder.imgSeparator1.visibility = View.VISIBLE
        } else {
            holder.translation.visibility = View.GONE
            holder.imgSeparator1.visibility = View.GONE
        }
        
        val fadlText = item.fadl
        if (fadlText.isNotEmpty()) {
            holder.fadl.text = fadlText
            holder.fadl.visibility = View.VISIBLE
            holder.imgSeparator2.visibility = View.VISIBLE
        } else {
            holder.fadl.visibility = View.GONE
            holder.imgSeparator2.visibility = View.GONE
        }
        
        holder.itemView.setOnClickListener { onItemClick() }
        holder.itemRoot.setOnClickListener { onItemClick() }
        holder.translation.setOnClickListener { onItemClick() }
        holder.content.setOnClickListener { onItemClick() }
        holder.fadl.setOnClickListener { onItemClick() }
    }


    fun setFontSize(size: Float) {
        fontSize = size
        notifyDataSetChanged()
    }

    fun getCount(position: Int): Int = counts[position]
    fun getTargetCount(position: Int): Int = list[position].count
    fun setCount(position: Int, count: Int) { counts[position] = count }
    fun getItem(position: Int): DhikrItem? = list.getOrNull(position)
    override fun getItemCount() = list.size
}
