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
    $limit = max(4, min(30, (int)($_GET['limit'] ?? 16)));

    $preferredCategoryIds = [];
    $preferredBrandIds = [];
    $preferredStyleWorldIds = [];
    $interactedProductIds = [];
    $signalCount = 0;

    if ($userId !== null || $guestId !== '') {
        if (MelvoreDB::tableExists('app_user_style_signals')) {
            $actorSql = $userId !== null ? 'user_id = ?' : 'guest_id = ?';
            $actorVal = $userId ?? $guestId;
            $weightCol = MelvoreDB::columnExists('app_user_style_signals', 'signal_weight')
                ? 'signal_weight'
                : (MelvoreDB::columnExists('app_user_style_signals', 'weight') ? 'weight' : '1');
            $sStmt = $pdo->prepare(
                "SELECT style_world_id, category_id, product_id, SUM($weightCol) AS total_w
                 FROM app_user_style_signals
                 WHERE $actorSql
                 GROUP BY style_world_id, category_id, product_id
                 ORDER BY total_w DESC
                 LIMIT 40"
            );
            $sStmt->execute([$actorVal]);
            foreach ($sStmt->fetchAll() as $sr) {
                $signalCount++;
                if (!empty($sr['category_id'])) {
                    $preferredCategoryIds[] = (int)$sr['category_id'];
                }
                if (!empty($sr['style_world_id'])) {
                    $preferredStyleWorldIds[] = (int)$sr['style_world_id'];
                }
                if (!empty($sr['product_id'])) {
                    $interactedProductIds[] = (int)$sr['product_id'];
                }
            }
        }

        if (MelvoreDB::tableExists('app_user_brand_activity')) {
            $actorSql = $userId !== null ? 'user_id = ?' : 'guest_id = ?';
            $actorVal = $userId ?? $guestId;
            $orderCol = MelvoreDB::columnExists('app_user_brand_activity', 'last_viewed_at') ? 'last_viewed_at' : 'created_at';
            $bStmt = $pdo->prepare(
                "SELECT brand_id FROM app_user_brand_activity
                 WHERE $actorSql
                 ORDER BY $orderCol DESC
                 LIMIT 10"
            );
            $bStmt->execute([$actorVal]);
            foreach ($bStmt->fetchAll() as $br) {
                $signalCount++;
                $preferredBrandIds[] = (int)$br['brand_id'];
            }
        }

        if ($userId !== null && MelvoreDB::tableExists('wishlist')) {
            $wStmt = $pdo->prepare('SELECT p.category_id, p.brand_id, w.product_id FROM wishlist w INNER JOIN products p ON p.product_id = w.product_id WHERE w.user_id = ? LIMIT 15');
            $wStmt->execute([$userId]);
            foreach ($wStmt->fetchAll() as $wr) {
                $signalCount++;
                if (!empty($wr['category_id'])) {
                    $preferredCategoryIds[] = (int)$wr['category_id'];
                }
                if (!empty($wr['brand_id'])) {
                    $preferredBrandIds[] = (int)$wr['brand_id'];
                }
                $interactedProductIds[] = (int)$wr['product_id'];
            }
        }
    }

    $preferredCategoryIds = array_values(array_unique(array_filter($preferredCategoryIds)));
    $preferredBrandIds = array_values(array_unique(array_filter($preferredBrandIds)));
    $preferredStyleWorldIds = array_values(array_unique(array_filter($preferredStyleWorldIds)));
    $interactedProductIds = array_values(array_unique(array_filter($interactedProductIds)));

    $isPersonalized = ($signalCount >= 2) && (!empty($preferredCategoryIds) || !empty($preferredBrandIds) || !empty($preferredStyleWorldIds));

    $recommendedProducts = [];
    if ($isPersonalized) {
        $conds = [];
        $params = [];
        if (!empty($preferredCategoryIds)) {
            $ph = implode(',', array_fill(0, count($preferredCategoryIds), '?'));
            $conds[] = "p.category_id IN ($ph)";
            $params = array_merge($params, $preferredCategoryIds);
        }
        if (!empty($preferredBrandIds)) {
            $ph = implode(',', array_fill(0, count($preferredBrandIds), '?'));
            $conds[] = "p.brand_id IN ($ph)";
            $params = array_merge($params, $preferredBrandIds);
        }
        if (!empty($conds)) {
            $orClause = '(' . implode(' OR ', $conds) . ')';
            $sql = "SELECT p.*, c.name AS category_name, c.slug AS category_slug, b.name AS brand_name, b.slug AS brand_slug
                    FROM products p
                    LEFT JOIN categories c ON c.category_id = p.category_id
                    LEFT JOIN brands b ON b.brand_id = p.brand_id
                    WHERE p.is_active = 1 AND $orClause
                    ORDER BY p.is_featured DESC, p.rating_average DESC, p.product_id DESC
                    LIMIT ?";
            $stmt = $pdo->prepare($sql);
            $idx = 1;
            foreach ($params as $val) {
                $stmt->bindValue($idx++, $val, PDO::PARAM_INT);
            }
            $stmt->bindValue($idx, $limit, PDO::PARAM_INT);
            $stmt->execute();
            $recommendedProducts = MelvoreProductFormatter::formatRows($stmt->fetchAll());
        }
    }

    // Honest trending/editorial fallback when insufficient personalization signals exist
    if (empty($recommendedProducts)) {
        $isPersonalized = false;
        $fStmt = $pdo->prepare(
            'SELECT p.*, c.name AS category_name, c.slug AS category_slug, b.name AS brand_name, b.slug AS brand_slug
             FROM products p
             LEFT JOIN categories c ON c.category_id = p.category_id
             LEFT JOIN brands b ON b.brand_id = p.brand_id
             WHERE p.is_active = 1
             ORDER BY p.view_count DESC, p.is_featured DESC, p.rating_average DESC
             LIMIT ?'
        );
        $fStmt->bindValue(1, $limit, PDO::PARAM_INT);
        $fStmt->execute();
        $recommendedProducts = MelvoreProductFormatter::formatRows($fStmt->fetchAll());
    }

    // Recently viewed brands
    $recentBrands = [];
    if (!empty($preferredBrandIds)) {
        $bPh = implode(',', array_fill(0, count($preferredBrandIds), '?'));
        $rbStmt = $pdo->prepare("SELECT * FROM brands WHERE brand_id IN ($bPh) AND status = 'active'");
        $rbStmt->execute($preferredBrandIds);
        foreach ($rbStmt->fetchAll() as $rb) {
            $recentBrands[] = [
                'brand_id' => (int)$rb['brand_id'],
                'name' => (string)$rb['name'],
                'slug' => (string)$rb['slug'],
                'logo_url' => MelvoreResponse::mediaUrl($rb['logo'] ?? null),
                'description' => (string)($rb['description'] ?? ''),
            ];
        }
    }

    // Favourite styles
    $favouriteStyles = [];
    if (!empty($preferredStyleWorldIds) && MelvoreDB::tableExists('app_style_worlds')) {
        $sPh = implode(',', array_fill(0, count($preferredStyleWorldIds), '?'));
        $swStmt = $pdo->prepare("SELECT style_world_id, slug, name, tagline, cover_image_url, accent_color FROM app_style_worlds WHERE style_world_id IN ($sPh) AND is_active = 1");
        $swStmt->execute($preferredStyleWorldIds);
        foreach ($swStmt->fetchAll() as $sw) {
            $favouriteStyles[] = [
                'style_world_id' => (int)$sw['style_world_id'],
                'slug' => (string)$sw['slug'],
                'name' => (string)$sw['name'],
                'tagline' => (string)($sw['tagline'] ?? ''),
                'cover_image_url' => MelvoreResponse::mediaUrl($sw['cover_image_url'] ?? null),
                'accent_color' => (string)($sw['accent_color'] ?? '#C8CCD4'),
            ];
        }
    }

    MelvoreResponse::ok([
        'is_personalized' => $isPersonalized,
        'title' => $isPersonalized ? 'Curated For You' : 'Trending & Editorial Picks',
        'subtitle' => $isPersonalized
            ? 'Tailored from your style worlds, brands, and saved pieces'
            : 'Explore trending drops across Melvore',
        'products' => $recommendedProducts,
        'recent_brands' => $recentBrands,
        'favourite_styles' => $favouriteStyles,
    ], 'For You feed loaded');
} catch (Throwable $e) {
    MelvoreResponse::error('Unable to load personalized feed.', 'SERVER_ERROR', 500);
}
