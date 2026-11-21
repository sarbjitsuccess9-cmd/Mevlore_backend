<?php
declare(strict_types=1);

require_once __DIR__ . '/response.php';

/**
 * Validated image/video upload helper using finfo MIME inspection.
 */
final class MelvoreMediaUpload
{
    private const IMAGE_MIME_MAP = [
        'image/jpeg' => 'jpg',
        'image/png' => 'png',
        'image/webp' => 'webp',
    ];

    public static function handleImageUpload(string $fieldName, string $subDir, int $maxBytes = 5_242_880): string
    {
        if (!isset($_FILES[$fieldName]) || !is_array($_FILES[$fieldName])) {
            MelvoreResponse::error('No image file uploaded.', 'UPLOAD_MISSING', 400);
        }
        $file = $_FILES[$fieldName];
        if (($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
            MelvoreResponse::error('Image upload failed with error code ' . (int)($file['error'] ?? -1), 'UPLOAD_ERROR', 400);
        }
        $size = (int)($file['size'] ?? 0);
        if ($size <= 0 || $size > $maxBytes) {
            MelvoreResponse::error('Image size must be under 5 MB.', 'FILE_TOO_LARGE', 422);
        }
        $tmpPath = (string)($file['tmp_name'] ?? '');
        if ($tmpPath === '' || !is_uploaded_file($tmpPath)) {
            MelvoreResponse::error('Invalid upload payload.', 'INVALID_UPLOAD', 400);
        }

        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $mime = (string)$finfo->file($tmpPath);
        if (!isset(self::IMAGE_MIME_MAP[$mime])) {
            MelvoreResponse::error('Unsupported image format. Allowed: JPG, PNG, WEBP.', 'UNSUPPORTED_MEDIA_TYPE', 415);
        }

        $ext = self::IMAGE_MIME_MAP[$mime];
        $safeSub = preg_replace('/[^a-zA-Z0-9_\-]/', '', $subDir);
        $uploadRoot = MelvoreEnv::get('UPLOAD_ROOT_DIR', dirname(__DIR__, 2) . '/uploads');
        $targetDir = rtrim($uploadRoot, '/') . '/' . $safeSub;
        if (!is_dir($targetDir) && !mkdir($targetDir, 0755, true) && !is_dir($targetDir)) {
            MelvoreResponse::error('Unable to prepare upload storage.', 'STORAGE_ERROR', 500);
        }

        $filename = 'mlv_' . date('Ymd_His') . '_' . bin2hex(random_bytes(8)) . '.' . $ext;
        $destPath = $targetDir . '/' . $filename;
        if (!move_uploaded_file($tmpPath, $destPath)) {
            MelvoreResponse::error('Failed to store uploaded file.', 'STORAGE_ERROR', 500);
        }

        $publicPrefix = rtrim(MelvoreEnv::get('UPLOAD_PUBLIC_PREFIX', '/uploads'), '/');
        return $publicPrefix . '/' . $safeSub . '/' . $filename;
    }
}
