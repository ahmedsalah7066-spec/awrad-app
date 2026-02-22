
Add-Type -AssemblyName System.Drawing

$sourcePath = "c:\Users\ahmed\AndroidStudioProjects\awrad\google_play_icon.png"
$resDir = "c:\Users\ahmed\AndroidStudioProjects\awrad\app\src\main\res"

$iconSizes = @{
    "mipmap-mdpi"    = 48
    "mipmap-hdpi"    = 72
    "mipmap-xhdpi"   = 96
    "mipmap-xxhdpi"  = 144
    "mipmap-xxxhdpi" = 192
}

$foregroundSizes = @{
    "drawable-mdpi"    = 108
    "drawable-hdpi"    = 162
    "drawable-xhdpi"   = 216
    "drawable-xxhdpi"  = 324
    "drawable-xxxhdpi" = 432
}

$img = [System.Drawing.Image]::FromFile($sourcePath)

# 1. Generate Legacy Icons (Square and Round)
foreach ($key in $iconSizes.Keys) {
    $size = $iconSizes[$key]
    $outputDir = Join-Path $resDir $key
    
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    }

    # Square Icon
    $squareBitmap = New-Object System.Drawing.Bitmap($size, $size)
    $graph = [System.Drawing.Graphics]::FromImage($squareBitmap)
    $graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graph.DrawImage($img, 0, 0, $size, $size)
    $squareBitmap.Save((Join-Path $outputDir "ic_launcher.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $graph.Dispose()
    $squareBitmap.Dispose()
    Write-Host "Saved $key/ic_launcher.png"

    # Round Icon
    $roundBitmap = New-Object System.Drawing.Bitmap($size, $size)
    $graph = [System.Drawing.Graphics]::FromImage($roundBitmap)
    $graph.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddEllipse(0, 0, $size, $size)
    $graph.SetClip($path)
    $graph.DrawImage($img, 0, 0, $size, $size)
    
    $roundBitmap.Save((Join-Path $outputDir "ic_launcher_round.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $graph.Dispose()
    $roundBitmap.Dispose()
    $path.Dispose()
    Write-Host "Saved $key/ic_launcher_round.png"
}

# 2. Generate Adaptive Icon Foreground
# For adaptive icons, the foreground should be 108x108dp (108px at mdpi).
# The safe zone is the center 72x72dp (66%).
# We will resize the image to fit within the safe zone (approx 70% of the full size) to avoid cropping.

foreach ($key in $foregroundSizes.Keys) {
    $size = $foregroundSizes[$key]
    # Extract density folder name (e.g., drawable-mdpi)
    # Note: Foreground drawables usually go into drawable-nodpi or drawable-xxxhdpi, 
    # but for best practice we can put them in density buckets or just use a high-res one in drawable-nodpi.
    # Here we will generate for each density to be safe.
    
    $outputDir = Join-Path $resDir $key
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    }

    $bitmap = New-Object System.Drawing.Bitmap($size, $size)
    $graph = [System.Drawing.Graphics]::FromImage($bitmap)
    $graph.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    
    # Scale image to 70% of the canvas size to fit in safe zone
    $scaleFactor = 0.7
    $imgSize = [int]($size * $scaleFactor)
    $offset = [int](($size - $imgSize) / 2)
    
    $graph.DrawImage($img, $offset, $offset, $imgSize, $imgSize)
    
    $bitmap.Save((Join-Path $outputDir "ic_launcher_foreground.png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $graph.Dispose()
    $bitmap.Dispose()
    Write-Host "Saved $key/ic_launcher_foreground.png"
}

$img.Dispose()
