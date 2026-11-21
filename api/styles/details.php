<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/db.php';
require_once dirname(__DIR__, 2) . '/includes/response.php';
require_once dirname(__DIR__, 2) . '/includes/auth.php';
require_once dirname(__DIR__, 2) . '/includes/product_formatter.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $userId = MelvoreAuth::getCurrentUserId();
    $guestId = MelvoreAuth::getGuestId();

    $styleId = (int)($_GET['id'] ?? ($_GET['style_world_id'] ?? 0));
    $slug = trim((string)($_GET['slug'] ?? ''));
    $page = max(1, (int)($_GET['page'] ?? 1));
    $limit = max(1, min(60, (int)($_GET['limit'] ?? 24)));
    $offset = ($page - 1) * $limit;

    if ($styleId <= 0 && $slug === '') {
        MelvoreResponse::error('Style world id or slug is required.', 'VALIDATION_ERROR', 422);
    }
    if (!MelvoreDB::tableExists('app_style_worlds')) {
        MelvoreResponse::error('Style world catalog is not configured.', 'NOT_FOUND', 404);
    }

    if ($styleId > 0) {
        $stmt = $pdo->prepare('SELECT * FROM app_style_worlds WHERE style_world_id = ? AND is_active = 1 LIMIT 1');
        $stmt->execute([$styleId]);
    } else {
        $stmt = $pdo->prepare('SELECT * FROM app_style_worlds WHERE slug = ? AND is_active = 1 LIMIT 1');
        $stmt->execute([$slug]);
    }
    $row = $stmt->fetch();
    if (!$row) {
        MelvoreResponse::error('Style world not found.', 'NOT_FOUND', 404);
    }
    $wid = (int)$row['style_world_id'];

    // Record exploration signal
    if (($userId !== null || $guestId !== '') && MelvoreDB::tableExists('app_user_style_signals')) {
        $sigStmt = $pdo->prepare(
            'INSERT INTO app_user_style_signals (user_id, guest_id, style_world_id, signal_type, signal_weight, created_at)
             VALUES (?, ?, ?, "style_explore", 2.0, NOW())'
        );
        $sigStmt->execute([$userId, $guestId !== '' ? $guestId : null, $wid]);
    }

    $products = [];
    $total = 0;
    if (MelvoreDB::tableExists('app_style_world_products')) {
        $cntStmt = $pdo->prepare(
            'SELECT COUNT(DISTINCT p.product_id)
             FROM app_style_world_products swp
             INNER JOIN products p ON p.product_id = swp.product_id
             WHERE swp.style_world_id = ? AND p.is_active = 1'
        );
        $cntStmt->execute([$wid]);
        $total = (int)$cntStmt->fetchColumn();

        $pStmt = $pdo->prepare(
            'SELECT p.*, c.name AS category_name, c.slug AS category_slug, b.name AS brand_name, b.slug AS brand_slug
             FROM app_style_world_products swp
             INNER JOIN products p ON p.product_id = swp.product_id
             LEFT JOIN categories c ON c.category_id = p.category_id
             LEFT JOIN brands b ON b.brand_id = p.brand_id
             WHERE swp.style_world_id = ? AND p.is_active = 1
             ORDER BY swp.display_order ASC, p.is_featured DESC, p.product_id DESC
             LIMIT ? OFFSET ?'
        );
        $pStmt->bindValue(1, $wid, PDO::PARAM_INT);
        $pStmt->bindValue(2, $limit, PDO::PARAM_INT);
        $pStmt->bindValue(3, $offset, PDO::PARAM_INT);
        $pStmt->execute();
        $products = MelvoreProductFormatter::formatRows($pStmt->fetchAll());
    }

    // Fallback via app_tags matching style slug if no direct mapping rows exist
    if (empty($products) && $total === 0 && MelvoreDB::tableExists('app_tags') && MelvoreDB::tableExists('app_product_tag_map')) {
        $tagKey = strtolower((string)$row['slug']);
        $pStmt = $pdo->prepare(
            'SELECT DISTINCT p.*, c.name AS category_name, c.slug AS category_slug, b.name AS brand_name, b.slug AS brand_slug
             FROM products p
             INNER JOIN app_product_tag_map ptm ON ptm.product_id = p.product_id
             INNER JOIN app_tags t ON t.tag_id = ptm.tag_id
             LEFT JOIN categories c ON c.category_id = p.category_id
             LEFT JOIN brands b ON b.brand_id = p.brand_id
             WHERE p.is_active = 1 AND (LOWER(t.slug) = ? OR LOWER(t.name) LIKE ?)
             ORDER BY p.is_featured DESC, p.product_id DESC
             LIMIT ? OFFSET ?'
        );
        $pStmt->bindValue(1, $tagKey, PDO::PARAM_STR);
        $pStmt->bindValue(2, '%' . $tagKey . '%', PDO::PARAM_STR);
        $pStmt->bindValue(3, $limit, PDO::PARAM_INT);
        $pStmt->bindValue(4, $offset, PDO::PARAM_INT);
        $pStmt->execute();
        $products = MelvoreProductFormatter::formatRows($pStmt->fetchAll());
        $total = count($products);
    }

    // Distinct categories inside this style world
    $catMap = [];
    foreach ($products as $pr) {
        if (!empty($pr['category_id']) && !empty($pr['category_name'])) {
            $catMap[(int)$pr['category_id']] = [
                'category_id' => (int)$pr['category_id'],
                'name' => (string)$pr['category_name'],
                'slug' => (string)($pr['category_slug'] ?? ''),
            ];
        }
    }

    $themeCfg = [];
    if (!empty($row['theme_config'])) {
        $decoded = is_string($row['theme_config']) ? json_decode($row['theme_config'], true) : $row['theme_config'];
        if (is_array($decoded)) {
            $themeCfg = $decoded;
        }
    }

    MelvoreResponse::ok([
        'style_world' => [
            'style_world_id' => $wid,
            'slug' => (string)($row['slug'] ?? ''),
            'name' => (string)($row['name'] ?? ''),
            'tagline' => (string)($row['tagline'] ?? ''),
            'description' => (string)($row['description'] ?? ''),
            'theme_key' => (string)($row['theme_key'] ?? 'dark_editorial'),
            'animation_key' => (string)($row['animation_key'] ?? 'smooth_reveal'),
            'font_style' => (string)($row['font_style'] ?? 'editorial_serif'),
            'primary_color' => (string)($row['primary_color'] ?? '#FFFFFF'),
            'accent_color' => (string)($row['accent_color'] ?? '#C8CCD4'),
            'background_color' => (string)($row['background_color'] ?? '#0A0A0D'),
            'cover_image_url' => MelvoreResponse::mediaUrl($row['cover_image_url'] ?? ($row['hero_image_url'] ?? null)),
            'mobile_image_url' => MelvoreResponse::mediaUrl($row['mobile_image_url'] ?? ($row['cover_image_url'] ?? null)),
            'video_url' => MelvoreResponse::mediaUrl($row['video_url'] ?? null),
            'theme_config' => $themeCfg,
        ],
        'categories' => array_values($catMap),
        'products' => $products,
        'pagination' => [
            'page' => $page,
            'limit' => $limit,
            'total' => $total,
            'total_pages' => max(1, (int)ceil($total / $limit)),
        ],
    ], 'Style world loaded');
} catch (Throwable $e) {
    MelvoreResponse::error('Unable to load style world.', 'SERVER_ERROR', 500);
}
