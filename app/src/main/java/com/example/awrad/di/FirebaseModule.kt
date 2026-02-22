package com.example.awrad.di

import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.FirebaseFirestoreSettings
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object FirebaseModule {
    
    @Provides
    @Singleton
    fun provideFirestoreInstance(): FirebaseFirestore {
        val firestore = FirebaseFirestore.getInstance()
        
        // Configure Firestore settings
        val settings = FirebaseFirestoreSettings.Builder()
        .setLocalCacheSettings(com.google.firebase.firestore.PersistentCacheSettings.newBuilder().build())
        .build()
        
        firestore.firestoreSettings = settings
        
        return firestore
    }
}
